# autoparser configuration schema

*Schema for autoparser configuration*

## Properties

- **`name`** *(string)*: Name of the configuration.
- **`description`** *(string)*: Description of the configuration.
- **`choice_delimiter`** *(string)*: Delimiter used to separate integer -> value mappings. Used by parse_choices() to generate values mapping.
- **`choice_delimiter_map`** *(string)*: Delimiter used to separate integer from value. Used by parse_choices() to generate values mapping.
- **`categorical_types`** *(array)*: List of categorical types according to data dictionary. Categorical field types are used by single_field_mapping() to infer whether values or references to values mapping should be set.
  - **Items** *(string)*
- **`text_types`** *(array)*: List of non-categorical (textual) types according to data dictionary. Text field types are used as a hint to single_field_mapping() to _not_ set a values mapping.
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
