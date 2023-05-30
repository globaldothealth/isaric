# ISARIC Clinical Data Model

[![parsers](https://github.com/globaldothealth/isaric/actions/workflows/parsers.yml/badge.svg)](https://github.com/globaldothealth/isaric/actions/workflows/parsers.yml)

ISARIC Clinical Data Model development. This repository has the
[schemas](schemas/dev) and [parser](isaric/parsers) specifications. For the
parsing library that does the data transformation, see
[adtl](https://github.com/globaldothealth/adtl).

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
field mappings that are parsed by
[adtl](https://github.com/globaldothealth/adtl). The parser TOML (or JSON) file
follows the adtl
[specification](https://github.com/globaldothealth/adtl/blob/main/docs/specification.md).

## How to use these

To transform the input files (usually database snapshots from REDCap), install
[adtl](https://github.com/globaldothealth/adtl). Use `adtl --help` to look at
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

### Development

Install [pre-commit](https://pre-commit.com) and setup pre-commit hooks
(`pre-commit install`) which will do linting checks before commit.
