# ISARIC Clinical Data Model

ISARIC Clinical Data Model development.

## Setup

Clone the repository

    git clone git@github.com:globaldothealth/isaric.git

You'll need Python>=3.10 installed to run this application. Switch to the
cloned repository folder before the following steps.

### Method 1: Using Poetry

We use [poetry](https://python-poetry.org) to manage package dependencies

1. If you are on macOS with [`brew`](https://brew.sh) installed, you can
   `brew install poetry`. Or, using the official installer: `curl -sSL
   https://install.python-poetry.org | python3 -`.
2. Run `poetry install` to install the dependencies.

If this does not work, try using requirements.txt

### Method 2: Using requirements.txt

1. Create a virtual environment: `python3 -m venv`
2. Switch to the virtual environment: `source venv/bin/activate`
3. Install from requirements.txt: `pip install -r requirements.txt`

## Structure

```shell
.
├── docs
│   └── spec-format.md
├── isaric  # Python module
│   ├── parser.py             # main program
│   ├── parsers               # specification files used by parser.py
│   │   └── isaric-ccpuk.json
│   ├── schemas.py            # pydantic schemas
│   └── taxonomy              # categorical classifications
│       └── v1.json
├── notebooks                 # Jupyter notebooks
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests                     # unit tests
    └── test_example.py
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

**Note**: If you used the requirements.txt method for installation, then the
above will not work. Replace `poetry run isaric-parser` with `python3 -m
isaric.parser` in the instructions. This will run the `__main__` component of
the [isaric.parser](isaric/parser.py) module.

### Development

Install [pre-commit](https://pre-commit.com) and setup pre-commit hooks
(`pre-commit install`) which will do linting checks before commit.
