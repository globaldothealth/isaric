import io
import re
import csv
import json
import logging
import hashlib
import argparse
from typing import Optional, Any, Union
from collections import defaultdict
from pathlib import Path
from enum import Enum

import pint
from tqdm import tqdm


class Table(str, Enum):  # will be StrEnum from Python 3.11
    subject = "subject"
    visit = "visit"
    # observation = "observation"  # uncomment when observation is enabled


def get_value(row: dict[str, Any], rule: Union[str, dict[str, Any]]) -> Any:
    """Gets value from row using rule

    Same as get_value_unhashed(), except it hashes if sensitive = True in rule.
    This function should be used instead of get_value_unhashed() for
    application code.
    """
    value = get_value_unhashed(row, rule)
    if isinstance(rule, dict) and rule.get("sensitive") and value is not None:
        return hash_sensitive(value)
    else:
        return value


def get_value_unhashed(row: dict[str, Any], rule: Union[str, dict[str, Any]]) -> Any:
    """Gets value from row using rule (unhashed)

    Unlike get_value() this function does NOT hash sensitive data
    and should not be called directly, except for debugging. Use
    get_value() instead.
    """
    if isinstance(rule, str):  # constant
        return rule
    if "field" in rule:
        # do not parse field if condition is not met
        if "if" in rule and not parse_if(row, rule["if"]):
            return None
        value = row[rule["field"]]
        if "values" in rule:
            value = rule["values"].get(value)
        if "source_unit" in rule and "unit" in rule:  # perform unit conversion
            source_unit = get_value(row, rule["source_unit"])
            unit = rule["unit"]
            print(f"Will convert from {source_unit} to {unit}")
            try:
                value = pint.Quantity(float(value), source_unit).to(unit).m
            except ValueError:
                logging.error(f"Could not convert {value} to a floating point")
                raise
        return value
    elif "combinedType" in rule:
        return get_combined_type(row, rule)
    elif "otherField" in rule:
        logging.info("otherField not supported, returning None")
        return None
    else:
        raise ValueError(f"Could not return value for {rule}")


def matching_fields(fields: list[str], pattern: str) -> list[str]:
    "Returns fields matching pattern"
    compiled_pattern = re.compile(pattern)
    return [f for f in fields if compiled_pattern.match(f)]


def parse_if(row: dict[str, Any], rule: dict[str, Any]) -> bool:
    "Parse conditional statements and return a boolean"

    n_keys = len(rule.keys())
    assert n_keys == 1
    key = next(iter(rule.keys()))
    if key == "any" and isinstance(rule[key], list):
        return any(parse_if(row, r) for r in rule[key])
    elif key == "all" and isinstance(rule[key], list):
        return all(parse_if(row, r) for r in rule[key])
    attr_value = row[key]
    if isinstance(rule[key], dict):
        cmp = next(iter(rule[key]))
        value = rule[key][cmp]
        if cmp == ">":
            return attr_value > value
        elif cmp == ">=":
            return attr_value >= value
        elif cmp == "<":
            return attr_value < value
        elif cmp == "<=":
            return attr_value <= value
        elif cmp == "!=":
            return attr_value != value
        elif cmp in ["=", "=="]:
            return attr_value == value
        else:
            raise ValueError(f"Unrecognized operand: {cmp}")
    else:
        value = rule[key]
        return attr_value == value


def get_list(row: dict[str, Any], rule: dict[str, Any]) -> list[Any]:
    """Gets values from row for a combinedType: list rule"""

    assert "fields" in rule
    assert len(rule["fields"]) >= 1
    rules = []

    # expand fieldPattern rules
    for r in rule["fields"]:
        if "fieldPattern" in r:
            for match in matching_fields(list(row.keys()), r.get("fieldPattern")):
                rules.append({"field": match, **r})
        else:
            rules.append(r)
    return [get_value(row, r) for r in rules]


def get_combined_type(row: dict[str, Any], rule: dict[str, Any]):
    """Gets value from row for a combinedType rule.

    A rule with the combinedType key combines multiple fields in the row
    to get the value. Thus this rule assumes that the combinedType fields
    do NOT have repeated (possibly different) values across the dataset.

    Example of dataset that will be handled correctly, with modliv and
    mildliver being the categorical indicators for moderate and mild
    liver disease respectively:

        subjid,modliv,mildliver,otherfield
        1,0,1,NA
        1,,,

    Example of dataset that will not be handled correctly:

        subjid,modliv,mildliver,otherfield
        1,0,,
        1,,1,

    For a combinedType rule to successfully run, all the field values should
    be present in the same row.
    """
    assert "combinedType" in rule
    combined_type = rule["combinedType"]
    rules = rule["fields"]
    if combined_type == "all":
        return all(get_value(row, r) for r in rules)
    elif combined_type == "any":
        return any(get_value(row, r) for r in rules)
    elif combined_type == "firstNonNull":
        try:
            return next(filter(None, [get_value(row, r) for r in rules]))
        except StopIteration:
            return None
    elif combined_type == "list":
        return get_list(row, rule)
    else:
        raise ValueError(f"Unknown {combined_type} in {rule}")


def hash_sensitive(value: str) -> str:
    """Hashes sensitive values. This is not generally sufficient for
    anonymisation, as the value still serves as a unique identifier,
    but is better than storing the value unprocessed."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class Parser:

    # We don't have unique subject ID, as the same subject could be
    # re-admitted and get a different subjid:
    # https://github.com/globaldothealth/isaric/issues/12

    subject: dict[str, Any] = defaultdict(dict)
    visit: dict[str, Any] = defaultdict(dict)
    fieldnames: dict[str, list[str]] = {}

    def __init__(self, spec: str):
        if ".json" not in spec:  # look in relative path
            if (
                possible_spec := Path(__file__).parent / "parsers" / f"{spec}.json"
            ).exists():
                spec = str(possible_spec)
        with open(spec) as fp:
            self.spec = json.load(fp)
        if "study" not in self.spec:
            raise ValueError("Parser specification missing required 'study' element")
        if "subject" not in self.spec:
            raise ValueError("Parser specification missing required 'subject' element")
        # visits and observations not implemented yet
        self.study = self.spec.get("study")
        for table in Table:
            self.fieldnames[table.value] = list(self.spec[table.value].keys())

    def update_subjects(self, row):
        primary_key_field = self.spec["primaryKey"]["subject"]
        primary_key = row[self.spec["subject"][primary_key_field]["field"]]
        for attr in self.spec["subject"]:
            if (value := get_value(row, self.spec["subject"][attr])) is not None:
                self.subject[primary_key][attr] = value

    def update_visits(self, row):
        primary_key_field = self.spec["primaryKey"]["visit"]
        primary_key = row[self.spec["visit"][primary_key_field]["field"]]
        for attr in self.spec["visit"]:
            if (value := get_value(row, self.spec["visit"][attr])) is not None:
                self.visit[primary_key][attr] = value

    def parse(self, file: str):
        self.clear()
        with open(file) as fp:
            reader = csv.DictReader(fp)
            for row in tqdm(
                reader,
                desc=f"[{self.spec['name']}] parsing {Path(file).name}",
            ):
                self.update_subjects(row)
                self.update_visits(row)
        self.validate()
        return self

    def validate(self):
        "Use schemas to validate data"
        pass

    def clear(self):
        "Clears parser state"
        self.subject = defaultdict(dict)

    def write_csv(
        self,
        table: Table,
        output: Optional[str] = None,
    ) -> str | None:
        "Writes to output as CSV a particular table"

        def writerows(fp, table):
            writer = csv.DictWriter(fp, fieldnames=self.fieldnames[table])
            writer.writeheader()
            for i in getattr(self, table):
                writer.writerow(getattr(self, table)[i])
            return fp

        if output:
            with open(output, "w") as fp:
                writerows(fp, table)
            return None
        else:
            buf = io.StringIO()
            return writerows(buf, table).getvalue()

    def save(self, output: Optional[str] = None):
        "Saves all tables to CSV"

        for table in Table:
            self.write_csv(table, f"{output}-{table.value}.csv")


def main():
    cmd = argparse.ArgumentParser(
        prog="isaric-parser",
        description="Parses clinical data into ISARIC schema as CSV given a specification",
    )
    cmd.add_argument(
        "spec",
        help="Specification file to use, can also take a parser name located in isaric/parsers",
    )
    cmd.add_argument("file", help="File to read in")
    cmd.add_argument(
        "-o", "--output", help="Output file, if blank, writes to standard output"
    )
    args = cmd.parse_args()
    if output := Parser(args.spec).parse(args.file).save(args.output):
        print(output)


if __name__ == "__main__":
    main()
