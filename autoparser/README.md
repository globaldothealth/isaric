# autoparser

autoparser helps in the generation of [ISARIC parsers](../isaric/parsers) as
TOML files, which can then be processed by
[adtl](https://github.com/globaldothealth/adtl) to transform files from the
source schema to the [ISARIC schema](../schemas/dev).

It comprises two programs:

1. **autoparser create-mapping**: Creates the initial mapping from the data dictionary and
   ISARIC schema. The mapping is generated as a CSV file with the following
   [fields](#intermediate-csv-schema).

2. **autoparser create-parser**: Uses the intermediate CSV mapping to create the TOML file
   that can be used by adtl. Usually there are false matches in the intermediate
   mapping, which errs on including fields rather than excluding so that
   curators only have to delete the field mappings that are not relevant. After
   this deletion process, the output TOML can be further inspected and adtl run
   to ensure data conforms to the ISARIC schema.

**Specifying schema path**: autoparser requires location of schemas, this can be
set either using `--schema-path` option to autoparser-csv or autoparser-toml, or
by exporting the `ISARIC_SCHEMA_PATH` variable in the environment:

```shell
export ISARIC_SCHEMA_PATH=/Users/a/sources/isaric
```

If you are running autoparser from within the root of the isaric repository,
then the default schema path should work out of the box.

## Installation

If you have [`pipx`](https://pypa.github.io/pipx/) installed (recommended, install using `brew install pipx` on macOS):

```shell
pipx install 'git+https://github.com/globaldothealth/isaric#egg=autoparser&subdirectory=autoparser'
```

Alternatively you can use `pip`, replace `pipx` with `pip`, but this will
install autoparser's dependencies into your global Python environment which
could cause issues with other packages.

This will install `autoparser`. If this is not
found, run `pipx ensurepath` to fix, which inform the terminal about the
installation location for the scripts.

**Alternatively**, one can run autoparser from a clone of the Git repository

``shell
python3 -m autoparser
``

## Parser construction process

1. **Data**: Get the data as CSV or Excel and the data dictionary
1. **Preparing the data dictionary**: If the data dictionary is not in CSV, or
   split across multiple Excel sheets, then it needs to be combined to a single
   CSV.
1. **Creating autoparser config**: Optional step if the data is not in REDCap
   (English) format. The autoparser config ([example](redcap-en.toml),
   [schema](#autoparser-config-schema)) specifies most of the variable
   configuration settings for autoparser.
1. **Generate intermediate mappings (CSV)**: Run with config and data dictionary
   to generate mappings:

   ```shell
   autoparser create-mapping <path to data dictionary> -o <parser-name>
   ```

   Here, `-o` sets the output name, and will create
   `<parser-name>-<table-name>.csv` where table-name is one of subject, visit,
   observation. For optional arguments (such as using a custom configuration
   which was created in step 3), see `autoparser-csv --help`

1. **Curate mappings**: The intermediate mappings must be manually curated, as
   autoparser-csv generates false matches. In most cases, deleting mismatched
   field mappings will suffice, though there may be cases when a field mappings
   needs to be added manually. Cases where more than one field in the data
   correspond to a single ISARIC schema field (such as `has_liver_disease` being
   a `combinedType=any` combination of moderate and mild liver disease) are
   represented in the intermediate mapping by having more than one row for a
   single ISARIC `schema_field`.

1. **Generate TOML**: This step is automated and should produce a TOML file that
   conforms to the [parser schema](../schemas/dev/parser.schema.json). The
   script attempts to generate correct information based on language cues
   (mapping yes to true, no to false) and field types.

   For example:

   ```shell
   autoparser create-toml parser-subject.csv parser-visit.csv parser-observation.csv -n parser
   ```

   will create `parser.toml` (specified using the `-n` flag) from the
   intermediate mappings for the subject, visit and observation tables.

1. **Review TOML**: The TOML file may contain errors, so it is recommended to
   check it and alter as necessary. At present, autoparser does not map the ID
   fields or the adtl header, so those should be checked, among other
   [limitations](#limitations).

1. **Run adtl**: Run adtl on the TOML file and the data source. This process
   will report validation errors, which can be fixed by reviewing the TOML file
   and looking at the source data that is invalid.

Alternatively, one can use the **graphical parser generator** to generate the TOML
file directly. Currently this is not integrated into the autoparser process, so
either one of the workflows have to be used for parser construction.

## Limitations

autoparser does not update the adtl header according to information from the
data dictionary. Also, it has limited support for the observation table, and no
support yet for parsing conditions that are specified with `if` statements.

## Autoparser config schema

- **`name`** *(string)*: Name of the configuration.
- **`description`** *(string)*: Description of the configuration.
- **`choice_delimiter`** *(string)*: Delimiter used to separate integer -> value mappings. Used by parse_choices() to generate values mapping.
- **`choice_delimiter_map`** *(string)*: Delimiter used to separate integer from value. Used by parse_choices() to generate values mapping.
- **`categorical_types`** *(array)*: List of categorical types according to data dictionary. Categorical field types are used by single_field_mapping() to infer whether values or references to values mapping should be set.
  - **Items** *(string)*
- **`text_types`** *(array)*: List of non-categorical (textual) types according to data dictionary. Text field types are used as a hint to single_field_mapping() to *not* set a values mapping.
  - **Items** *(string)*
- **`lang`** *(object)*: Language specific settings.
  - **`is_missing`** *(array)*: Denotes missing values.
    - **Items** *(string)*
  - **`is_true`** *(array)*: Denotes true or yes values.
    - **Items** *(string)*
  - **`is_false`** *(array)*: Denotes false or no values.
    - **Items** *(string)*
  - **`stopwords`** *(array)*: Words to ignore when matching or when generating TF-IDF matrix.
    - **Items** *(string)*
- **`schemas`** *(object)*: Schema mappings.
  - **`subject`** *(string)*: Schema for the subject mapping.
  - **`visit`** *(string)*: Schema for the visit mapping.
  - **`observation`** *(string)*: Schema for the observation mapping.
- **`scores`** *(object)*: Scores used by csv_mapping to order mappings.
  - **`*`** *(integer)*
- **`column_mappings`** *(object)*: Mappings of intermediate CSV to source data dictionary fields.
  - **`schema_field`** *(string)*: Field in the ISARIC schema that this mapping corresponds to.
  - **`field`** *(string)*: Field in the source data file that corresponds to the ISARIC schema field.
  - **`category`** *(string)*: Field category according to source.
  - **`description`** *(string)*: Field description.
  - **`choices`** *(string)*: Delimited field -> value mappings.
  - **`note`** *(string)*: Field note.
  - **`valid_type`** *(string)*: Field validation type according to source.
  - **`valid_min`** *(string)*: Minimum value for field if applicable.
  - **`valid_max`** *(string)*: Whether field is identifier.
  - **`is_identifier`** *(string)*: Whether field is identifier.
  - **`condition`** *(string)*: Field condition, when field is shown.
  - **`is_required`** *(string)*: Whether field is required in the source form.
- **`observation_type_mapping`** *(object)*: Mapping from source types to observation fields.
  - **`*`**: Must be one of: `['is_present', 'value', 'text']`.
