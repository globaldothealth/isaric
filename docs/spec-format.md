# Specification format

The specification file describes the field mappings from the source file to the
ISARIC schemas defined in [isaric/schemas.py](../isaric/schemas.py). The format
is under development and expected to change.

Specification files are located under [isaric/parsers](../isaric/parsers).
Specification files are in JSON and have the suffix `.json`.

Each specification file can refer to one or more tables defined in the [ISARIC
schema](../isaric/schemas.py)

**Required fields**. These metadata fields are defined at the top level of the specification

* **name**: Name of the specification, usually the source data name in
  lowercase and hyphenated. By convention, this is the same name as the
  specification file.
* **description**: Description of the specification
* **primaryKey**: Key value dictionary with keys as the table name and value as
  the primary key for the table. The primary key should be guaranteed to be
  unique within the table.

Each table within the ISARIC schema has its associated field mappings.

### study

Key value pairs describing the study table

### subject

Keys are **fields / attributes** in the ISARIC schema. Values are **rules**
that describe the mapping from the source data format. There are several valid
rule patterns, listed below. Each rule will either have a `field` attribute
that is the corresponding field in the source format, or a `combinedField`
attribute which links multiple fields in the source format, and specifies how
the fields should be combined. Fields can be marked as privacy sensitive using
`sensitive: true`, which can be used by the parser to take additional steps,
such as hashing the field.

* **Constant**: Every value in the table is the same constant value
  ```json
  { "country_iso3": "GBR" }
  ```

* **Single field**: Maps to a single field from the source format
  ```json
  {
    "date_death": {
      "field": "flw_date_death",
      "description": "Date of death"
     }
  }

* **Single field with mapping**: Same as **Single field**, but with an extra
  `values` key that describes the mapping from the values to the ones in the
  schema. This covers boolean fields, with the mappings being to `true` | `false` | `null`.
  ```json
  {
    "sex_at_birth": {
      "field": "sex",
      "values": {
        "1": "male",
        "2": "female",
        "3": "non_binary"
      },
      "description": "Sex at Birth"
    }
  }
  ```

  ```json
  {
    "has_dementia": {
      "field": "dementia_mhyn",
      "values": {
        "1": true,
        "2": false,
        "3": null
      },
      "description": "Dementia"
    }
  }
  ```

* **Combined type**: Refers to multiple fields in the source format. Requires
  a `combinedType` attribute specifying the combination criteria, and
  a `fields` attribute which a list of fields that will be combined.
  Accepted values for `combinedType` are:
  (i) *any* - Whether any of the fields are non-null (truthy)
  (i) *all* - Whether all of the fields are non-null (truthy)
  (i) *firstNonNull* - First in the list of fields that has a non-null value

  ```json
  {
    "has_liver_disease": {
      "combinedType": "any",
      "fields": [
        {
          "field": "modliv",
          "values": {
            "1": true,
            "0": false,
            "2": null
          },
          "description": "Moderate liver disease"
        },
        {
          "field": "mildliver",
          "values": {
            "1": true,
            "0": false,
            "2": null
          },
          "description": "Mild liver disease"
        }
      ]
    }
  }
  ```


### visit

### observation
