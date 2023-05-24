"""
Create draft intermediate mapping in CSV from source dataset to target dataset
"""
import os
import json
import copy
import argparse
from pathlib import Path
from typing import Dict, Any, List, Union

import tomli
import numpy as np
import pandas as pd
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer

from .util import maybe, parse_choices, DEFAULT_CONFIG


def matches_redcap(
    config: Dict[str, Any],
    data_dictionary: Union[pd.DataFrame, str],
    table: str,
    num_matches: int = 6,
) -> pd.DataFrame:
    column_mappings = {v: k for k, v in config["column_mappings"].items()}
    stopwords = config["lang"]["stopwords"]
    schema = get_fields(config, table)
    scores = config["scores"]

    lem = WordNetLemmatizer()

    def lemmatized(s, split=None):
        s = str(s).strip()
        return " ".join(lem.lemmatize(w) for w in s.split(sep=split))

    def lemmatized_choices(s: str) -> str:
        choices, _ = parse_choices(config, s)
        if choices is None:
            return " "
        else:
            return " " + " ".join(
                lemmatized(c) for c in choices.values() if isinstance(c, str)
            )

    if isinstance(data_dictionary, str):
        data_dictionary = Path(data_dictionary)
        if data_dictionary.suffix == ".csv":
            df = pd.read_csv(data_dictionary)
        elif data_dictionary.suffix == ".xlsx":
            df = pd.read_excel(data_dictionary)
        else:
            raise ValueError(f"Unsupported format (not CSV or XLSX): {data_dictionary}")
        df = df.rename(columns=column_mappings)[list(column_mappings.values())]
        df["description"] = df.description.map(lemmatized)
        df["lemmatized_choices"] = df.choices.map(lemmatized_choices)

    # Drop field types like 'banner' which are purely informative
    _allowed_field_types = config["categorical_types"] + config["text_types"]
    df = df[df.type.isin(_allowed_field_types)]

    # Initial scoring (tf_rank column) using TF-IDF similarity
    vec = TfidfVectorizer(
        stop_words=stopwords,
        max_df=0.9,
        ngram_range=(1, 2),
    )
    properties = [p for p in list(schema["properties"].keys()) if "_id" not in p]
    descriptions = [
        " ".join(
            [
                lemmatized(attr, split="_"),
                schema["properties"][attr].get("description", ""),
            ]
        )
        for attr in properties
    ]

    # Use the data dictionary to set up the vocabulary and do the initial TF-IDF
    # which is used to transform the field names
    X = vec.fit_transform(df.description + df.lemmatized_choices)
    Y = vec.transform(descriptions)

    # Similarity
    D = Y.dot(X.T)

    # Keep 'num_matches' top matches in terms of similarity
    S = np.argsort(D.toarray(), axis=1)[:, ::-1][:, :num_matches]

    # First draft of match data
    match_df = pd.DataFrame(
        columns=["schema_field", "field", "tf_rank"],
        data=sum(
            [
                [
                    [
                        properties[i],
                        df.iloc[k].field,
                        num_matches - j,
                    ]
                    for j, k in enumerate(S[i])
                ]
                for i in range(len(descriptions))
            ],
            [],
        ),
    )
    match_df["table"] = table

    # Merge data dictionary into match_df for further scoring
    match_df = match_df.merge(df, on="field")

    # We can return match_df here, but we can put in some manual hints for
    # refining tf_rank, based on matching field types:
    #
    # score=3 for type match (dropdown/radio == booleans/enums, text otherwise)
    # score=3 for both being dates
    # score=-3 for only one of the fields being a date, extremely unlikely match
    # score=1 for every token that is not a stopword appearing in the source field / description

    # scoring using pre-defined rules
    def scorer(row) -> int:
        "Returns a score for a match row"
        score = 1  # default score, every match gets this
        if row["table"] == "observation":
            return row["tf_rank"]  # no type information available here yet
        attributes = schema["properties"][row["schema_field"]]
        T = attributes.get("type")
        if T == "boolean":
            score += (
                scores["type-match"]
                if row["type"] in ["dropdown", "radio", "yesno"]
                else scores["type-mismatch"]
            )
        if (
            (T == "string" and row["type"] == "text")
            or (T == "number" and row["type"] == "decimal")
            or ("enum" in attributes and row["type"] == "categorical")
            or T == row["type"] == "integer"
        ):
            score += scores["type-match"]
        if attributes.get("format") == "date":
            score += (
                scores["type-match"]
                if ("date_" in str(row.get("valid_type", "")) or T == "date")
                else scores["date-mismatch"]
            )
        if (
            "follow" in row.get("category", "")
        ):  # de-emphasise followup, usually only required in observation
            score += scores["is-followup"]
        words = row["schema_field"].split("_")
        score += sum(
            w in row["field"] + " " + row["description"]
            for w in set(words) - set(stopwords)
        )
        return score * row["tf_rank"]

    match_df["score"] = match_df.apply(scorer, axis=1)
    return match_df.sort_values(["schema_field", "score"], ascending=[True, False])


def deep_get(d: Dict[str, Any], keys: str) -> Any:
    dc = copy.deepcopy(d)
    ks = keys.split(".")
    for k in ks:
        dc = dc[k]
    return dc


def read_json(file: str) -> Dict:
    with (Path(__file__).parent / file).open() as fp:
        return json.load(fp)


def get_fields(config: Dict[str, Any], table: str) -> List[str]:
    schemas = config.get("schemas", [])
    if table not in schemas:
        raise ValueError(f"Schema not found for table: {table}")
    if table != "observation":
        return read_json(config["schema-path"] / schemas[table])
    else:
        return {
            "properties": {
                k: {"category": "observation"}
                for k in deep_get(
                    read_json(config["schema-path"] / schemas[table]),
                    "properties.name.enum",
                )
            }
        }


def accuracy(
    table: str, parser_spec: Dict[str, Any], mapping: pd.DataFrame, accuracy_mode="any"
) -> float:
    "Returns proportion of first-choice mappings that are present in the parser"
    if table not in parser_spec:
        raise ValueError(f"Parser specification has no entries for table {table}")
    if table == "observation":
        raise NotImplementedError("Observation support not implemented yet")

    def _get_fields(rule):
        if "field" in rule:
            return [rule["field"]]
        if "combinedType" in rule:
            return [r["field"] for r in rule["fields"]]

    parser_mapping = {
        attr: _get_fields(parser_spec[table][attr]) for attr in parser_spec[table]
    }
    # drop constant fields
    parser_mapping = {k: v for k, v in parser_mapping.items() if v is not None}

    if accuracy_mode == "any":
        matches = mapping.groupby("schema_field")["field"].apply(list).to_dict()
    elif accuracy_mode == "first":
        matches = mapping.groupby("schema_field")["field"].first().to_dict()

    correct_matches = 0
    incorrect_matches = []
    for attr in parser_mapping:
        if (fields := matches.get(attr)) is None:
            continue
        if isinstance(fields, str):
            if fields in parser_mapping[attr]:
                correct_matches += 1
            else:
                incorrect_matches.append(attr)
        elif isinstance(fields, list):
            if set(fields) & set(parser_mapping[attr]):
                correct_matches += 1
            else:
                incorrect_matches.append(attr)

    return correct_matches / len(parser_mapping), incorrect_matches


def main():
    parser = argparse.ArgumentParser(
        description="Generate intermediate CSV used by make_toml.py (create-parser) to create TOML",
        prog="autoparser create-mapping",
    )
    parser.add_argument("dictionary", help="Data dictionary to use")
    parser.add_argument(
        "-o", "--output", help="Name to use for output files", default="isaric"
    )
    parser.add_argument(
        "-n",
        "--num_matches",
        help="Number of matches to output for each field",
        type=int,
        default=6,
    )
    parser.add_argument("--schema-path", help="Path where ISARIC schemas are located")
    parser.add_argument(
        "-t", "--tables", help="Only match for tables (comma separated list, no spaces)"
    )
    parser.add_argument(
        "-c", "--config", help=f"Configuration file to use (default={DEFAULT_CONFIG})"
    )
    parser.add_argument("-k", "--check", help="Parser TOML to check accuracy against")
    parser.add_argument(
        "--accuracy-mode",
        help="Accuracy mode: 'any' (default) checks whether any field matches, "
        "'first' checks whether the first preference matches",
        choices=["any", "first"],
        default="any",
    )
    args = parser.parse_args()
    with maybe(args.config, Path, default=Path(__file__).parent / DEFAULT_CONFIG).open(
        "rb"
    ) as fp:
        config = tomli.load(fp)
        config["schema-path"] = (
            maybe(args.schema_path, Path)
            or maybe(os.getenv("ISARIC_SCHEMA_PATH"), Path)
            or Path.cwd()
        )
    tables = args.tables.split(",") if args.tables else config["schemas"].keys()
    parser_spec = None
    if args.check:
        with open(args.check, "rb") as fp:
            parser_spec = tomli.load(fp)
    for table in tables:
        df = matches_redcap(
            config,
            args.dictionary,
            table,
            num_matches=args.num_matches,
        )
        if not args.check:
            df.to_csv(f"{args.output}-{table}.csv", index=False)
        else:
            if table == "observation":
                continue  # not implemented
            acc, incorrect_matches = accuracy(
                table, parser_spec, df, accuracy_mode=args.accuracy_mode
            )
            print(
                f"Accuracy [{args.accuracy_mode}]  ({table}): {acc:.2%}, incorrect matches:"
            )
            print("\n".join("\t" + s for s in incorrect_matches))


if __name__ == "__main__":
    main()
