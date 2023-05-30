"""
Generate TOML parser from intermediate CSV file
"""
import os
import re
import json
import argparse
import functools
import logging
import operator
from pathlib import Path
from typing import Dict, List, Any, Tuple

import pandas as pd

from .util import maybe, parse_choices, read_data, DEFAULT_CONFIG
from .toml_writer import dump


def adtl_header(
    name: str, description: str, schema_version: str = "dev", definitions={}
):
    return {
        "adtl": {
            "name": name,
            "description": description,
            "tables": {
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


@functools.lru_cache
def get_schema(schema_path: Path) -> Dict[str, Any]:
    return read_data(schema_path)["properties"]


def get_type_enum(config: Dict[str, Any], table: str, field: str):
    "Returns field types and enums from a field in a table"

    schema = get_schema(
        schema_path := Path(config["schema-path"]) / config["schemas"][table]
    )
    if field not in schema:
        raise ValueError(
            f"get_type_enum(): {field!r} field not in {table!r} schema, from {schema_path}"
        )
    if "enum" in schema[field]:
        return "enum", schema[field]["enum"]
    else:
        return schema[field].get("type", "string"), []


def single_field_mapping(
    config: Dict[str, Any],
    match: pd.core.frame.pandas,
    references: Dict[str, Any],
    use_type: str = None,
    add_auto_condition=False,
) -> Dict[str, Any]:
    try:
        choices, nulls = parse_choices(config, match.choices)
    except ValueError as e:
        logging.warning(e)
        choices, nulls = None, []
    out = {"field": match.field, "description": match.description}
    if not use_type:  # auto detect type from schema field type
        schema_field_type, schema_field_enum = get_type_enum(
            config, match.table, match.schema_field
        )
    else:
        schema_field_type, schema_field_enum = use_type, []
    if match.type in config["categorical_types"] and choices:
        if (choice_key := json.dumps(choices, sort_keys=True)) in references:
            out["ref"] = references[choice_key]
        else:
            out["values"] = choices

    if (
        schema_field_type == "enum"
        and schema_field_enum
        and (out.get("values") or out.get("ref"))
    ):
        if out.get("ref"):
            # re-expand references to enable map_enum() to work
            backref = [k for k in references if references[k] == out["ref"]][0]
            out["values"] = json.loads(backref)
            del out["ref"]
        mapped_enum = map_enum(list(out["values"].values()), schema_field_enum)
        out["values"] = {
            k: mapped_enum[v] for k, v in out["values"].items() if v in mapped_enum
        }
        if mapped_enum:
            print(
                f"\n* {match.schema_field!r} from {match.field!r}, one of {schema_field_enum!r}"
            )
            for s, t in mapped_enum.items():
                print(f"  - {s} → {t}")

    # Only add auto-generated condition if flag enabled and we have not already
    # added a condition, usually from a condition column in the data dictionary
    if add_auto_condition and "if" not in out:
        if "values" not in out or not nulls:  # text field
            out["if"] = {match.field: {"!=": ""}}
        elif len(nulls) > 1:
            out["if"] = {"all": [{match.field: {"!=": n}} for n in nulls]}
        else:
            out["if"] = {match.field: {"!=": nulls[0]}}
        if out.get("ref") == "Y/N/NK":  # most common case
            out["if"] = {match.field: {"!=": 3}}

    return out


def make_toml_table(
    config: Dict[str, Any],
    mappings: pd.DataFrame,
    table: str,
    references: Dict[str, Any],
) -> Dict[str, Any]:
    "Make TOML table (observation handling is separate)"
    if table == "observation":
        return _make_toml_observation(config, mappings, table, references)

    mappings = mappings[mappings.table == table]
    if mappings.empty:
        return {}
    outmap = {}

    for field, field_matches in mappings.groupby("schema_field"):
        field_type, field_enum = get_type_enum(config, table, field)
        if len(field_matches) == 1:  # single field
            outmap[field] = single_field_mapping(
                config,
                field_matches.iloc[0],
                references,
            )

        else:  # combinedType
            if isinstance(field_type, list):  # field can be of multiple types
                if "array" in field_type:
                    field_type = "array"
                elif "boolean" in field_type:
                    field_type = "boolean"
                else:
                    field_type = field_type[0]
            outmap[field] = {
                "combinedType": {"array": "list", "boolean": "any"}.get(
                    field_type, "firstNonNull"
                ),
                "fields": [
                    single_field_mapping(
                        config,
                        match,
                        references,
                    )
                    for match in field_matches.itertuples()
                ],
            }

    return {table: outmap}


def _make_toml_observation(
    config: Dict[str, Any],
    mappings: pd.DataFrame,
    table: str,
    references: Dict[str, Any],
) -> Dict[str, Any]:
    assert table == "observation"
    mappings = mappings[mappings.table == "observation"]
    observations = []

    for mapping in mappings.itertuples():
        if "category" in mappings.columns:
            phase = map_enum(
                [mapping.category.replace("treatment", "study")],
                ["admission", "study", "followup"],
            )
            phase = phase.get(mapping.category, "study")
        else:
            phase = "study"  # no category information found, default to study
        obs_type = config["observation_type_mapping"].get(mapping.type, "value")
        field_mapping = single_field_mapping(
            config, mapping, references, use_type=mapping.type, add_auto_condition=True
        )

        # Move if to observation block instead of in the mapping
        condition = field_mapping["if"]
        del field_mapping["if"]
        observations.append(
            {
                "name": mapping.schema_field,
                "phase": phase,
                "date": {
                    "ref": {
                        "admission": "admissionDateHierarchy",
                        "study": "dailyDateHierarchy",
                        "followup": "followupDateHierarchy",
                    }.get(phase)
                },
                "if": condition,
                obs_type: field_mapping,
            }
        )
    return {"observation": observations}


def make_toml(
    config: Dict[str, Any],
    mappings: pd.DataFrame,
    name: str,
    tables: List[str] = ["subject", "visit", "observation"],
    description: str = None,
):
    references, definitions = common_mappings(config, mappings)
    data = adtl_header(name, description or name, definitions=definitions)
    for table in tables:
        data.update(make_toml_table(config, mappings, table, references))
    return data


def map_enum(keys: List[str], sources: List[str]) -> Dict[str, str]:
    def score(key, source):
        key = re.split("-|_| ", str(key).lower())
        source = re.split("-|_| ", source.lower())
        return sum(
            sum(
                [
                    [int(s.startswith(w) or s.endswith(w)) * len(w) for s in source]
                    for w in key
                ],
                [],
            )
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
    config: Dict[str, Any], mappings: pd.DataFrame, top: int = 3
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    mappings.choices.value_counts()[:3]
    references = {}
    definitions = {}

    def _parse_choices(s):
        c, _ = parse_choices(config, s)
        return json.dumps(c, sort_keys=True) if c else None

    # use value_counts() on parsed_choices instead of choices to
    # normalise various flavours of Y/N/NK or Y/N/NA
    mappings["parsed_choices"] = mappings.choices.map(_parse_choices)
    top_mappings = mappings.parsed_choices.value_counts()[:top].index

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


def write_toml(data: Dict[str, Any], output: str):
    with open(output, "wb") as fp:
        dump(data, fp)


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
        help=f"Configuration file to use (default={DEFAULT_CONFIG})",
        type=Path,
    )
    parser.add_argument("--schema-path", help="Path where ISARIC schemas are located")

    args = parser.parse_args()
    mappings = pd.concat((pd.read_csv(f) for f in args.mappings), ignore_index=True)
    config = read_data(
        maybe(args.config, Path, default=Path(__file__).parent / DEFAULT_CONFIG)
    )
    config["schema-path"] = (
        maybe(args.schema_path, Path)
        or maybe(os.getenv("ISARIC_SCHEMA_PATH"), Path)
        or Path.cwd()
    )

    write_toml(make_toml(config, mappings, args.name), f"{args.name}.toml")


if __name__ == "__main__":
    main()
