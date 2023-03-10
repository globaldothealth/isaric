"""
Create draft intermediate mapping in CSV from source dataset to target dataset
"""
import json
import copy
import argparse
from pathlib import Path

import tomli
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

from .util import maybe, json_get, DEFAULT_CONFIG


def matches_redcap(
    config: dict[str],
    data_dictionary: pd.DataFrame | str,
    table: str,
    num_matches: int = 6,
) -> pd.DataFrame:
    column_mappings = {v: k for k, v in config["column_mappings"].items()}
    stopwords = config["lang"]["stopwords"]
    schema = get_fields(config, table)
    scores = config["scores"]

    if isinstance(data_dictionary, str):
        df = pd.read_csv(data_dictionary).rename(columns=column_mappings)[
            list(column_mappings.values())
        ]
        df["description"] = df.description.map(str.strip)

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
    descriptions = [" ".join(attr.split("_")) for attr in properties]

    # Use the data dictionary to set up the vocabulary and do the initial TF-IDF
    # which is used to transform the field names
    X = vec.fit_transform(df.description)
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
            "follow" in row["category"]
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


def deep_get(d: dict, keys: str):
    dc = copy.deepcopy(d)
    ks = keys.split(".")
    for k in ks:
        dc = dc[k]
    return dc


def read_json(file: str) -> dict:
    with (Path(__file__).parent / file).open() as fp:
        return json.load(fp)


def get_fields(config: dict[str], table: str) -> list[str]:
    schemas = config.get("schemas", [])
    if table not in schemas:
        raise ValueError(f"Schema not found for table: {table}")
    if table != "observation":
        return read_json(schemas[table])
    else:
        return {
            "properties": {
                k: {"category": "observation"}
                for k in deep_get(read_json(schemas[table]), "properties.name.enum")
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate intermediate CSV used by make_toml.py to create TOML"
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
    parser.add_argument(
        "-t", "--tables", help="Only match for tables (comma separated list, no spaces)"
    )
    parser.add_argument(
        "-c", "--config", help=f"Configuration file to use (default={DEFAULT_CONFIG})"
    )
    args = parser.parse_args()
    with maybe(args.config, Path, default=Path(__file__).parent / DEFAULT_CONFIG).open(
        "rb"
    ) as fp:
        config = tomli.load(fp)
    tables = args.tables.split(",") if args.tables else config["schemas"].keys()
    for table in tables:
        df = matches_redcap(
            config,
            args.dictionary,
            table,
            num_matches=args.num_matches,
        )
        df.to_csv(f"{args.output}-{table}.csv", index=False)


if __name__ == "__main__":
    main()
