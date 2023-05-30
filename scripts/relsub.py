"""
REDCap RELSUB matcher
"""
import json
import csv
import uuid
import argparse
import itertools
from typing import Generator, Dict, Iterable, Union, Any, Callable


def serial_generator(start: int = 0) -> Generator[int, None, None]:
    while True:
        start += 1
        yield start


def uuid_generator() -> Generator[str, None, None]:
    while True:
        yield str(uuid.uuid4())


def relsub_matcher(
    data: Iterable[Dict[str, Any]],
    left_col: str,
    right_col: str,
    generator: Callable[[], Generator[Union[int, str], None, None]] = serial_generator,
    delimiter=";",
) -> Union[Dict[str, int], Dict[str, str]]:
    already_matched: Dict[str, str] = {}
    all_ids = set()
    for row in data:
        lefts = [s.strip() for s in row[left_col].split(delimiter)]
        rights = [s.strip() for s in row[right_col].split(delimiter)]
        for left, right in itertools.product(lefts, rights):
            if left == right:
                continue
            if left in already_matched:
                already_matched[right] = already_matched[left]
            else:
                already_matched[right] = left

        all_ids |= set(lefts + rights)
    uids = {}
    id_factory = generator()
    for v in sorted(set(already_matched.values())):
        uids[v] = next(id_factory)
    return {k: uids[already_matched.get(k, k)] for k in all_ids}


def relsub_matcher_file(
    file: str,
    left_col: str,
    right_col: str,
    generator: str = "serial",
    encoding="utf-8",
    delimiter=";",
):
    if generator == "serial":
        generator = serial_generator
    elif generator == "uuid":
        generator = uuid_generator
    else:
        raise ValueError("Supported generators are 'serial' or 'uuid'")
    with open(file, encoding=encoding) as fp:
        return relsub_matcher(
            csv.DictReader(fp),
            left_col,
            right_col,
            delimiter=delimiter,
            generator=generator,
        )


def main():
    parser = argparse.ArgumentParser(description="REDCap RELSUB matcher")
    parser.add_argument("file", help="RELSUB file to process")
    parser.add_argument("--left", help="Left column", default="USUBJID")
    parser.add_argument("--right", help="Right column", default="RSUBJID")
    parser.add_argument("--encoding", help="File encoding", default="utf-8-sig")
    parser.add_argument(
        "--delimiter",
        help="Delimiter for lists within left and right columns",
        default=";",
    )
    parser.add_argument(
        "--generator",
        help="ID generator to use",
        choices=["serial", "uuid"],
        default="serial",
    )
    parser.add_argument("-o", "--output", help="Output file", default="relsub.json")
    args = parser.parse_args()

    matches = relsub_matcher_file(
        args.file,
        args.left,
        args.right,
        generator=args.generator,
        encoding=args.encoding,
        delimiter=args.delimiter,
    )
    with open(args.output, "w") as fp:
        json.dump(matches, fp, indent=2, sort_keys=True)
    print("relsub.py: wrote", args.output)
    print(
        f"           {len(set(matches.values()))} unique IDs across {len(matches)} total"
    )


if __name__ == "__main__":
    main()
