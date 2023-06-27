"""
Data summary of source files used in ETL pipeline

Output is a JSON file with the following structure

```json
{
    "file": "CVOLRQ Antarctica 2023-04-05.csv"
    "sha256": "a98942bbcccdde9898924989901293aa111ff",
    "mimetype": "text/csv",
    "encoding": "utf-8-sig",
    "id_field": "record_id",
    "n_id": 6187,
    "non_empty_fields": [
        "record_id",
        "ethnicity",
        "diabetes_mhyn"
    ]
}
```
"""
import os
import json
import csv
import mimetypes
import hashlib
from typing import Any
from pathlib import Path
from argparse import ArgumentParser
from typing import Dict, Optional

DEFAULT_ENCODING = "utf-8-sig"


def sha256(filename: str) -> str:
    "Returns SHA-256 hash of the file"
    sha256 = hashlib.sha256()
    with open(filename, "rb") as f:
        while True:
            data = f.read(2048)
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()


def guess_mimetype_encoding(filename):
    mimetype, encoding = mimetypes.guess_type(filename)
    return mimetype, encoding or DEFAULT_ENCODING


def data_summary(
    filename: str, id_field: str, encoding: str = DEFAULT_ENCODING
) -> Dict[str, Any]:
    non_empty_fields = set()
    ids = set()
    with open(filename, encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            non_empty_fields |= {field for field in row if row[field].strip()}
            if row[id_field].strip():
                ids.add(row[id_field])
    return {"non_empty_fields": sorted(non_empty_fields), "n_id": len(ids)}


def main(
    filename: str, parser_name: str, id_field: str, encoding: Optional[str] = None
) -> Dict[str, Any]:
    mimetype, guessed_encoding = guess_mimetype_encoding(filename)
    encoding = encoding or guessed_encoding  # prefer encoding supplied by user
    isaric_data = os.getenv("ISARIC_DATA")
    return {
        "file": str(Path(filename).relative_to(isaric_data))
        if isaric_data
        else filename,
        "sha256": sha256(filename),
        "parser": parser_name,
        "mimetype": mimetype,
        "encoding": encoding,
        "id_field": id_field,
        **data_summary(filename, id_field, encoding),
    }


if __name__ == "__main__":
    parser = ArgumentParser(description="Source data summary")
    parser.add_argument(
        "parser_name", help="Location of the parser, relative to isaric root folder"
    )
    parser.add_argument("file", help="Filename to produce data summary for")
    parser.add_argument("id", help="ID (primary key) field in file")
    parser.add_argument(
        "-o", "--output-folder", help="Metadata output folder", default="metadata"
    )
    parser.add_argument("--encoding", help="Use encoding instead of auto-detecting")
    args = parser.parse_args()

    data = main(args.file, args.parser_name, args.id, args.encoding)
    output_file = Path(args.file).stem + ".json"

    if not (
        parent_folder := Path(args.output_folder) / Path(args.parser_name).stem
    ).exists():
        parent_folder.mkdir(parents=True)
    with open(parent_folder / output_file, "w") as fp:
        json.dump(data, fp, indent=2)
    print(json.dumps(data, indent=2))
