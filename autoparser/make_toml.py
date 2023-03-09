"""
Generate TOML parser from intermediate CSV file
"""
import re
import json
import argparse
import operator
from pathlib import Path

import tomli_w
import pandas as pd

MISSING = [
    "unknown",
    "n/a",
    "n/k",
    "na",
    "nk",
    "not applicable",
    "prefer not to say",
    "not specified",
    "not answered",
]
TRUE = ["y", "yes", "t", "true"]
FALSE = ["f", "false", "no", "n"]


def maybe(x, func, default=None):
    return func(x) if x is not None else default


def read_data(path: Path) -> dict:
    if path.suffix == ".json":
        with path.open() as fp:
            return json.load(fp)
    elif path.suffix == ".toml":
        with path.open("rb") as fp:
            return tomli.load(fp)


def adtl_header(
    name: str, description: str, schema_version: str = "dev", definitions={}
):
    return {
        "adtl": {
            "name": name,
            "description": description,
            "tables": {
                "study": {"kind": "constant"},
                "subject": {
                    "kind": "groupBy",
                    "groupBy": "subject_id",
                    "aggregation": "lastNotNull",
                    "schema": f"../../schemas/{schema_version}/subject.schema.json",
                },
                "visit": {
                    "kind": "groupBy",
                    "groupBy": "subject_id",
                    "aggregation": "lastNotNull",
                    "schema": f"../../schemas/{schema_version}/visit.schema.json",
                },
                "observation": {
                    "kind": "oneToMany",
                    "schema": f"../../schemas/{schema_version}/observation.schema.json",
                    "common": {"visit_id": {"field": "subjid", "sensitive": True}},
                },
            },
            **{"defs": definitions},
        }
    }


def parse_choices(s: str, delimiter: str, delimiter_map: str) -> dict[str]:
    lower_string = lambda s: s.strip().lower()
    if not isinstance(s, str):
        return None
    choices = dict(
        tuple(map(lower_string, x.split(delimiter_map)[:2])) for x in s.split(delimiter)
    )
    # drop n/a, n/k, unknowns
    choices = {k: v for k, v in choices.items() if v not in MISSING}
    for k, v in choices.items():
        if v in TRUE:
            choices[k] = True
        if v in FALSE:
            choices[k] = False
    return choices


def make_toml_table(
    config: dict[str],
    mappings: pd.DataFrame,
    table: str,
    references: dict[str],
    choice_delimiter="|",
    choice_delimiter_map=",",
) -> dict[str]:
    "Make TOML table (not observation, which is handled separately)"
    assert table in set(config["schemas"]) - {"observation"}
    schema = read_data(config["schemas"][table])["properties"]
    mappings = mappings[mappings.table == table]
    if mappings.empty:
        return {}
    outmap = {}

    def single_field_mapping(
        match: pd.core.frame.pandas, field_type: str, field_enum: list[str] = []
    ) -> dict[str]:
        out = {
            "field": match.source_field,
            "description": match.source_field_description,
        }
        if field_type in ["boolean", "enum"] and (
            choices := parse_choices(
                match.choices, choice_delimiter, choice_delimiter_map
            )
        ):
            if (choice_key := json.dumps(choices, sort_keys=True)) in references:
                out["ref"] = references[choice_key]
            else:
                out["values"] = choices

        if field_type == "enum" and field_enum and out.get("values"):
            mapped_enum = map_enum(list(out["values"].values()), field_enum)
            source_values = out["values"].copy()
            out["values"] = {
                k: mapped_enum[v] for k, v in out["values"].items() if v in mapped_enum
            }
            print(
                f"{match.source_field}\n"
                + "\n".join(
                    f"    {source} -> {target}"
                    for source, target in zip(
                        source_values.values(), out["values"].values()
                    )
                )
            )

        return out

    for field, field_matches in mappings.groupby("field"):
        field_type = schema[field].get("type")
        field_enum = schema[field].get("enum", [])
        if "enum" in schema[field]:
            field_type = "enum"
        if len(field_matches) == 1:  # single field
            outmap[field] = single_field_mapping(
                field_matches.iloc[0], field_type, field_enum
            )

        else:  # combinedType
            outmap[field] = {
                "combinedType": {"array": "list", "boolean": "any"}.get(
                    schema[field].get("type"), "firstNonNull"
                ),
                "fields": [
                    single_field_mapping(match, field_type, field_enum)
                    for match in field_matches.itertuples()
                ],
            }

    return {table: outmap}


def make_toml_observation(
    config: dict[str],
    mappings: pd.DataFrame,
) -> list[dict[str]]:
    mappings = mappings[mappings.table == "observation"]
    observation = []


def make_toml(
    config: dict[str],
    mappings: pd.DataFrame,
    name: str,
    tables: list[str] = ["subject", "visit"],
    description: str = None,
):
    references, definitions = common_mappings(
        mappings, delimiter="|", delimiter_map=","
    )
    data = adtl_header(name, description or name, definitions=definitions)
    for table in tables:
        if table != "observation":
            data.update(make_toml_table(config, mappings, table, references))
        else:
            data.update(make_toml_observation(config, mappings))
    return data


def map_enum(keys: list[str], sources: list[str]) -> dict[str, str]:
    def score(key, source):
        key = re.split("-|_| ", str(key).lower())
        source = re.split("-|_| ", source.lower())
        return sum(
            sum([[s.startswith(w) or s.endswith(w) for s in source] for w in key], [])
        )

    def max_score(key, sources):
        try:
            return max(
                (
                    (source, score(key, source))
                    for source in sources
                    if score(key, source) > 0
                ),
                key=operator.itemgetter(1),
            )[0]
        except ValueError:
            return None

    mapped_enum = {key: max_score(key, sources) for key in keys}
    return {k: v for k, v in mapped_enum.items() if v is not None}


def common_mappings(
    mappings: pd.DataFrame, delimiter: str, delimiter_map: str, top: int = 3
) -> tuple[dict[str], dict[str]]:
    mappings.choices.value_counts()[:3]
    references = {}
    definitions = {}

    def _parse_choices(s):
        c = parse_choices(s, delimiter, delimiter_map)
        return json.dumps(c, sort_keys=True) if c else None

    # use value_counts() on parsed_choices instead of choices to
    # normalise various flavours of Y/N/NK or Y/N/NA
    mappings["parsed_choices"] = mappings.choices.map(_parse_choices)
    top_mappings = mappings.parsed_choices.value_counts()[:top].index
    boolean_mapping_name = "Y/N/NK"

    # only add one boolean map for simplicity
    boolean_map_found = False
    for mapping in top_mappings:
        if boolean_map_found and "true" in mapping:
            continue
        if "true" in mapping:
            references[mapping] = "Y/N/NK"
            definitions["Y/N/NK"] = {"values": json.loads(mapping)}
            boolean_map_found = True
            continue
        c = json.loads(mapping)
        name = "/".join(map(str, c.values()))
        references[mapping] = name
        definitions[name] = {"values": c}
    return references, definitions


def write_toml(data: dict[str], output: str):
    with open(output, "wb") as fp:
        tomli_w.dump(data, fp)


def main():
    parser = argparse.ArgumentParser(
        description="Make TOML from intermediate CSV file created by csv_mapping.py"
    )
    parser.add_argument(
        "mappings", help="Mapping file(s) to create TOML from", nargs="+", type=str
    )
    parser.add_argument(
        "-n", "--name", help="Name of the parser (default=isaric)", default="isaric"
    )
    parser.add_argument(
        "-c",
        "--config",
        help="Configuration file to use (default=config.toml)",
        type=Path,
    )

    args = parser.parse_args()
    mappings = pd.concat((pd.read_csv(f) for f in args.mappings), ignore_index=True)

    with open(f"{args.name}.toml", "wb") as fp:
        tomli_w.dump(
            make_toml(
                read_data(
                    maybe(
                        args.config,
                        Path,
                        default=Path(__file__).with_name("config.toml"),
                    )
                ),
                mappings,
                args.name,
            ),
            fp,
        )


if __name__ == "__main__":
    main()
