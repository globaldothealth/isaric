"""
Generate TOML parser from intermediate CSV file
"""
import json
import argparse
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


def read_json(file: str | Path) -> dict:
    with open(file) as fp:
        return json.load(fp)


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
    schema = read_json(config["schemas"][table])["properties"]
    mappings = mappings[mappings.table == table]
    if mappings.empty:
        return {}
    outmap = {}

    def single_field_mapping(match: pd.core.frame.pandas, is_map: bool) -> dict[str]:
        out = {
            "field": match.source_field,
            "description": match.source_field_description,
        }
        if is_map and (
            choices := parse_choices(
                match.choices, choice_delimiter, choice_delimiter_map
            )
        ):
            if (choice_key := json.dumps(choices, sort_keys=True)) in references:
                out["ref"] = references[choice_key]
            else:
                out["values"] = choices
        return out

    for field, field_matches in mappings.groupby("field"):
        is_map = "enum" in schema[field] or schema[field]["type"] == "boolean"
        if len(field_matches) == 1:  # single field
<<<<<<< HEAD
            outmap[field] = single_field_mapping(field_matches[0], is_map)
=======
            outmap[field] = single_field_mapping(
                field_matches.iloc[0], field_type, field_enum
            )
>>>>>>> b7e1512 (fixup)

        else:  # combinedType
            outmap[field] = {
                "combinedType": {"array": "list", "boolean": "any"}.get(
                    schema[field].get("type"), "firstNonNull"
                ),
                "fields": [
                    single_field_mapping(match, is_map)
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
    args = parser.parse_args()
    mappings = pd.concat((pd.read_csv(f) for f in args.mappings), ignore_index=True)

    with open(f"{args.name}.toml", "wb") as fp:
        tomli_w.dump(
            make_toml(
                read_json(Path(__file__).with_name("config.json")),
                mappings,
                args.name,
            ),
            fp,
        )


if __name__ == "__main__":
    main()
