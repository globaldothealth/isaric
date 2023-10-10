# ISARIC Clinical Data Model

[![parsers](https://github.com/globaldothealth/isaric/actions/workflows/parsers.yml/badge.svg)](https://github.com/globaldothealth/isaric/actions/workflows/parsers.yml)

ISARIC Clinical Data Model development. This repository has the
[schemas](schemas/dev) and [parser](isaric/parsers) specifications. For the
parsing library that does the data transformation, see
[adtl](https://adtl.readthedocs.io).

## Schemas

Each table in the ISARIC schema has a corresponding JSON Schema
specification in [schemas](schemas). These schemas supersede the schemas.py file
in previous versions of this repository, as well as the taxonomy files, which
are now contained within the JSON schemas.

Schemas are versioned by the folder name (`dev`, `v1`, `v2`) under schemas. At
present, ISARIC schemas are under development, so they are located under `dev`.
Once the schema is finalised, it will be renamed to `v1`, following which only
additive changes will be performed on the schema. Breaking changes will require
a new version to be assigned.

## Parsers

Parser specification files, such as
[isaric-ccpuk](isaric/parsers/isaric-ccpuk.toml) under `parsers` describe the
field mappings that are parsed by adtl. The parser TOML (or JSON) file
follows the adtl
[specification](https://adtl.readthedocs.io/en/latest/specification.html).

## How to use these

To transform the input files (usually database snapshots from REDCap), install
[adtl](https://adtl.readthedocs.io/en/latest/getting_started/installation.html). Use `adtl --help` to look at
the options. As an example, to transform the REDCap data to the ISARIC schema
for the CCPUK study:

```shell
adtl isaric/parsers/isaric-ccpuk.toml data.csv
```

This will create a file `isaric-ccpuk-{table}.csv` for each table specified in
the specification file. The file prefix (`isaric-ccpuk`) can be changed by
passing the `-o` (`--output`) flag.
If a schema is specified for a particular table in the parser file, then adtl
uses it for validation. Validation status (true/false) and error messages are
reported in the `adtl_valid` and `adtl_error` columns in the output
respectively.

### Running with RELSUB matching

ISARIC source datasets have unique visit IDs, with every patient assigned a new
ID on every visit. There is a separate table (RELSUB in SDTM), which matches
visit IDs for the same subject. So if visit `A012` and `A342` refer to the same
patient, there would be an entry in the RELSUB table like: `A012,A342,SAME`. For
datasets that have relsub matching (`ref = "relsub"` present in subject ID
definition), we need to generate the RELSUB matching definition first, before
calling adtl with the RELSUB map. As an example, for the CCPUK RELSUB file
(corresponding [parser](isaric/parsers/isaric-ccpuk.toml)), this is the
procedure to transform the source data with RELSUB mapping:

```shell
# Create the RELSUB mapping
python3 scripts/relsub.py CCPUK_RELSUB.csv -o isaric-ccpuk-relsub.json
adtl isaric/parsers/isaric-ccpuk.toml ../isaric-data/ccpuk.csv --include-def isaric-ccpuk-relsub.json
```

The RELSUB script expects the ID columns to be named USUBJID, RSUBJID; these can
be changed via parameters, see `python3 scripts/relsub.py --help`.

### Development

Install [pre-commit](https://pre-commit.com) and setup pre-commit hooks
(`pre-commit install`) which will do linting checks before commit.
