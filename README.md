# ISARIC Clinical Data Model

ISARIC Clinical Data Model development.

## Setup

Clone the repository

    git clone git@github.com:globaldothealth/isaric.git


**Requirements**: Python >= 3.10, you will need to install
[poetry](https://python-poetry.org). If you are on macOS with
[`brew`](https://brew.sh) installed, you can `brew install poetry`. Or, using
the official installer: `curl -sSL https://install.python-poetry.org | python3 -`.

Run `poetry install` to install the dependencies.

## Structure

```shell
isaric
├── parser.py
├── parsers  # contains specification files used by parser.py
│   └── isaric-ccpuk.json
├── schemas.py  # pydantic schemas
└── taxonomy
    ├── __init__.py  # categorical classifications
    └── v1.json
```

The primary entry point of the application is
[isaric/parser.py](isaric/parser.py) which reads in data using a specified
*taxonomy* and *specification file* that describes the field mappings from the
source file to the ISARIC schemas defined in
[isaric/schemas.py](isaric/schemas.py).

**Taxonomy**: Taxonomy files, such as
[isaric/taxonomy/v1.json](isaric/taxonomy/v1.json) contain categorisations and
the canonical name used by the ISARIC schema for a particular category.
Taxonomy files are versioned in the filename, and with a `version` key in the
file to enable future extensibility.

**Specifications**: Specification files, such as
[isaric-ccpuk](isaric/parsers/isaric-ccpuk.json) under `parsers` describe the
field mappings. The full description of the specification file format is at
[docs/spec-format](docs/spec-format.md). The format is under development and
expected to change.

## Run

The parser is installed as the `isaric-parser` script within the poetry virtual
environment, and can be invoked by using `poetry run isaric-parser`.

```
$ poetry run isaric-parser --help

usage: isaric-parser [-h] [-o OUTPUT] spec file

Parses clinical data into ISARIC schema as CSV given a specification

positional arguments:
  spec                  Specification file to use, can also take a parser name located in isaric/parsers
  file                  File to read in

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file, if blank, writes to standard output
```

Currently there is only one specification written, with the Subject schema.

```shell
$ poetry run isaric-parser isaric-ccpuk data.csv --output output-ccpuk-subject.csv
[isaric-ccpuk] parsing CCPUK.csv: 14572it [00:01, 13092.82it/s]
```

### Development

Install [pre-commit](https://pre-commit.com) and setup pre-commit hooks
(`pre-commit install`) which will do linting checks before commit.
