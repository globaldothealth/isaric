"""
Check parser(s) against schemas for optional fields which are missing from
the parser. Creates a csv file and prints a condensed output for assessing
whether a parser is suitably complete.
Field is marked 'True' if it is present in the parser file.
"""

import json
import tomli
import pandas as pd
import argparse
import os

def get_observation_fields(schema: dict) -> list:
    try:
        return list(schema["properties"]["name"]["enum"])
    except KeyError:  # try oneOf
        return sum([
            obs["properties"]["name"]["enum"]
            if "enum" in obs["properties"]["name"]
            else [obs["properties"]["name"]["const"]]
            for obs in schema["oneOf"]
        ], [])

def check_table(table: str, schema: dict, parser: dict) -> dict:
    """
    Compares parser and schema for an indivdual table.
    """

    try:
        schema_fields = set(schema["properties"].keys())
        parser_fields = set(parser[table].keys())
    except AttributeError:  # observation table
        schema_fields = set(get_observation_fields(schema))
        parser_fields = set(item["name"] for item in parser[table])

    mismatch = schema_fields - parser_fields
    additional_fields = parser_fields - schema_fields

    return mismatch, additional_fields


def print_findings(name: str, missing: dict, lengths: dict, extras: dict):
    """
    Write to terminal
    """

    print(f"Summary of the missing optional fields for the {name} parser:")

    print("\n|table       \t|missing|total_fields |percentage_coverage|")
    print("|---------------|-------|-------------|-------------------|")
    for table in missing:
        print(
            f"|{table:14s}\t|{len(missing[table])}\t|{lengths[table]}\t      "
            f"|{(lengths[table]-len(missing[table]))/lengths[table]:%} |"
        )
    print()
    if (
        len(
            list(extras["subject"])
            + list(extras["visit"])
            + list(extras["observation"])
        )
        > 0
    ):
        print("There are fields no longer present in the schema in this parser:")
        print(
            f"Subject:{extras['subject']}\nVisit:{extras['visit']}\nObservation:{extras['observation']}"
        )
        print()


def missing_fields(parser_file: str, df: pd.DataFrame, schemas: tuple) -> pd.DataFrame:
    subject, visit, observation = schemas

    with open(parser_file, "rb") as pf:
        parser = tomli.load(pf)

    missing_fields = {}
    additional_fields = {}
    parser_name = parser["adtl"]["name"]

    for table, name in zip(
        [subject, visit, observation], ["subject", "visit", "observation"]
    ):
        missing_fields[name], additional_fields[name] = check_table(name, table, parser)

    missing_list = (
        list(missing_fields["subject"])
        + list(missing_fields["visit"])
        + list(missing_fields["observation"])
    )

    df[parser_name] = [
        (
            ""
            if fn in ["SUBJECT", "VISIT", "OBSERVATION"]  # creates blank line
            else (True if fn not in missing_list else False)
        )
        for fn in df["fieldname"]
    ]

    print_findings(
        parser_name,
        missing_fields,
        {
            "subject": len(subject["properties"]),
            "visit": len(visit["properties"]),
            "observation": len(get_observation_fields(observation))
        },
        additional_fields,
    )

    return df


def main():
    cmd = argparse.ArgumentParser(
        description="Checks which schema fields are present in a parser",
    )
    cmd.add_argument(
        "parser",
        help="Specification file/folder to use",
    )
    cmd.add_argument(
        "-a", "--all", help="Test all parsers in a given folder", action="store_true"
    )
    args = cmd.parse_args()

    subject_schema = "schemas/dev/subject.schema.json"
    visit_schema = "schemas/dev/visit.schema.json"
    observation_schema = "schemas/dev/observation.schema.json"

    subject, visit, observation = (
        json.load(open(sch, "rb"))
        for sch in [subject_schema, visit_schema, observation_schema]
    )

    df = pd.DataFrame(
        {
            "fieldname": ["SUBJECT"]
            + list(subject["properties"].keys())
            + ["VISIT"]
            + list(visit["properties"].keys())
            + ["OBSERVATION"]
            + get_observation_fields(observation)
        }
    )

    if args.all:
        directory = args.parser

        for filename in os.listdir(directory):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                df = missing_fields(f, df, (subject, visit, observation))

    else:
        df = missing_fields(args.parser, df, (subject, visit, observation))

    # write to csv
    df.to_csv("scripts/checkfields/check_fields.csv", index=False)


if __name__ == "__main__":
    main()
