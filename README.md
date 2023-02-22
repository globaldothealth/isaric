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
├── isaric  # Python module
│   ├── parsers               # specification files used by parser.py
│   │   └── isaric-ccpuk.toml
└── schemas/dev               # JSON schemas for tables
    └── subject.schema.json
    └── visit.schema.json
    └── observation.schema.json
├── notebooks                 # Jupyter notebooks
├── poetry.lock
├── pyproject.toml
├── README.md
└── tests                     # unit tests
    └── test_example.py
```

**Schemas**: Each table in the ISARIC schema has a corresponding JSON Schema
specification in [schemas](schemas). These schemas supersede the schemas.py file
in previous versions of this repository, as well as the taxonomy files, which
are now contained within the JSON schemas. Schemas are versioned by the folder
name (`dev`, `v1`, `v2`) under schemas. At present, ISARIC schemas are under
development, so they are located under `dev`. Once the schema is finalised, it
will be renamed to `v1`, following which only additive changes will be performed
on the schema. Breaking changes will require a new version to be assigned.

**Specifications**: Specification files, such as
[isaric-ccpuk](isaric/parsers/isaric-ccpuk.toml) under `parsers` describe the
field mappings that are parsed by [adtl](https://github.com/globaldothealth/adtl).
The parser TOML (or JSON) file follows the adtl
[specification](https://github.com/globaldothealth/adtl/blob/main/docs/specification.md).

## Run

To transform the input files (usually database snapshots from REDCap), install
[adtl](https://github.com/globaldothealth/adtl). Use `adtl --help` to look at
the options. As an example, to transform the REDCap data to the ISARIC schema
for the CCPUK study:

```shell
adtl isaric/parsers/isaric-ccpuk.toml data.csv -o output
```

### Development

Install [pre-commit](https://pre-commit.com) and setup pre-commit hooks
(`pre-commit install`) which will do linting checks before commit.
