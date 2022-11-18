import io
import csv
import json
import logging
import hashlib
import argparse
from typing import Any, Union
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm


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
        value = row[rule["field"]]
        if "values" in rule:
            return rule["values"].get(value)
        else:
            return value
    elif "combinedType" in rule:
        return get_combined_type(row, rule)
    elif "otherField" in rule:
        logging.info("otherField not supported, returning None")
        return None
    else:
        raise ValueError(f"Could not return value for {rule}")


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
    else:
        raise ValueError(f"Unknown {combined_type} in {rule}")


def hash_sensitive(value: str) -> str:
    """Hashes sensitive values. This is not generally sufficient for
    anonymisation, as the value still serves as a unique identifier,
    but is better than storing the value unprocessed."""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


class Parser:

    subject = defaultdict(dict)
    fieldnames = {}

    def __init__(self, spec: str):
        if ".json" not in spec:  # look in relative path
            if (
                possible_spec := Path(__file__).parent / "parsers" / f"{spec}.json"
            ).exists():
                spec = possible_spec
        with open(spec) as fp:
            self.spec = json.load(fp)
        if "study" not in self.spec:
            raise ValueError("Parser specification missing required 'study' element")
        if "subject" not in self.spec:
            raise ValueError("Parser specification missing required 'subject' element")
        # visits and observations not implemented yet
        self.study = self.spec.get("study")
        self.fieldnames["subject"] = list(self.spec["subject"].keys())

    def update_subjects(self, row):
        primary_key_field = self.spec["primaryKey"]["subject"]
        primary_key = row[self.spec["subject"][primary_key_field]["field"]]
        for attr in self.spec["subject"]:
            if (value := get_value(row, self.spec["subject"][attr])) is not None:
                self.subject[primary_key][attr] = value

    def parse(self, file: str):
        self.clear()
        with open(file) as fp:
            reader = csv.DictReader(fp)
            for row in tqdm(
                reader,
                desc=f"[{self.spec['name']}] parsing {Path(file).name}",
            ):
                self.update_subjects(row)
        self.validate()
        return self

    def validate(self):
        "Use schemas to validate data"
        pass

    def clear(self):
        "Clears parser state"
        self.subject = defaultdict(dict)

    def to_csv(self, output: str = None):
        "Writes data to CSV(s), or returns as string"

        if output:
            with open(output, "w") as fp:
                writer = csv.DictWriter(fp, fieldnames=self.fieldnames["subject"])
                writer.writeheader()
                for i in self.subject:
                    writer.writerow(self.subject[i])
                if not output:
                    return fp.getvalue()
        else:
            buf = io.StringIO()
            writer = csv.DictWriter(buf, fieldnames=self.fieldnames["subject"])
            writer.writeheader()
            for i in self.subject:
                writer.writerow(self.subject[i])
            return buf.getvalue()


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
    if output := Parser(args.spec).parse(args.file).to_csv(args.output):
        print(output)


if __name__ == "__main__":
    main()
