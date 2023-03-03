"""
Flag in CI if parser fails validation
"""

import sys
import json
from pathlib import Path
from typing import Tuple

import tomli
import fastjsonschema


def validate(file: str) -> Tuple[str, bool, str]:
    "Validates file and returns a tuple of whether file is valid and a string error message"
    schema_header = Path(file).read_text().split()[:2]
    if (
        schema_header[0] == "#:schema"
    ):  # hint to EvenBetterTOML, next line is the schema file
        schema_file_relative = schema_header[1]
        schema_file_path = Path(file).parent / schema_file_relative
        if not schema_file_path.exists():
            raise FileNotFoundError(f"Schema file not found at: {schema_file_path}")
        with schema_file_path.open() as fp:
            schema_validate = fastjsonschema.compile(json.load(fp))
    else:
        return file, False, "no schema found"

    with open(file, "rb") as fp:
        data = tomli.load(fp)
    try:
        schema_validate(data)
    except fastjsonschema.exceptions.JsonSchemaValueException as e:
        return file, False, e.message
    return file, True, ""


def message(file, valid, error_message):
    return f" OK\t{file}" if valid else f"ERR\t{file}\t{error_message}"


files = sys.argv[1:]
if not files:
    print(
        f"""usage: {sys.argv[0]} files...
    Validate parser file(s) according to schema directive"""
    )
    sys.exit(0)

any_invalid = False
for file, valid, error_message in map(validate, files):
    any_invalid |= not valid
    print(message(file, valid, error_message))

sys.exit(int(any_invalid))
