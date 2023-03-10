# autoparser

autoparser helps in the generation of [ISARIC parsers](../isaric/parsers) as
TOML files, which can then be processed by
[adtl](https://github.com/globaldothealth/adtl) to transform files from the
source schema to the [ISARIC schema](../schemas/dev).

It comprises two programs:

1. **autoparser-csv**: Creates the initial mapping from the data dictionary and
   ISARIC schema. The mapping is generated as a CSV file with the following
   [fields](#intermediate-csv-schema).

2. **autoparser-toml**: Uses the intermediate CSV mapping to create the TOML file
   that can be used by adtl. Usually there are false matches in the intermediate
   mapping, which errs on including fields rather than excluding so that
   curators only have to delete the field mappings that are not relevant. After
   this deletion process, the output TOML can be further inspected and adtl run
   to ensure data conforms to the ISARIC schema.

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
   to generate mappings
1. **Curate mappings**: The intermediate mappings must be manually curated, as
   autoparser-csv generates false matches. In most cases, deleting mismatched
   field mappings will suffice, though there may be cases when a field mappings
   matches a particular field in the ISARIC schema are common (example: needs to
   be added. Cases where more than one field in the data dictionary
   `has_liver_disease` being a boolean any combination of moderate and mild
   liver disease), and are represented in the intermediate mapping by having
   more than one row for a single ISARIC `schema_field`.
1. **Generate TOML**: This step is automated and should produce a TOML file that
   conforms to the [parser schema](../schemas/dev/parser.schema.json). The
   script attempts to generate correct information based on language cues
   (mapping yes to true, no to false) and field types.
1. **Review TOML**: The TOML file may contain small errors, so it is recommended
   to check it and alter as necessary.
1. **Run adtl**: Run adtl on the TOML file and the data source. This process
   will report on validation errors encountered, which can be fixed by reviewing
   the TOML file and looking at the source data that is invalid.

Alternatively, one can use the **graphical parser generator** to generate the TOML
file directly. Currently this is not integrated into the autoparser process, so
either one of the workflows have to be used for parser construction.

## Intermediate CSV schema

## Autoparser config schema
