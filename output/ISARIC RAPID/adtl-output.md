>adtl ../isaric/isaric/parsers/isaric-rapid.toml ../../ISARIC_files/ISARIC/ISARIC\ RAPID/ISARICCOVID19RAPIDFo_DATA_2022-07-06_0932.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |5530   |8061   |68.601910% |
|visit          |4911   |8061   |60.922962% |
|observation    |278937 |381839 |73.050946% |

## subject

* 2527: data must contain ['subject_id', 'country_iso3', 'enrolment_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 2: data.age must be bigger than or equal to 0
* 2: data.age must be smaller than or equal to 120

## visit

* 3150: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 102899: data must contain ['phase', 'date', 'name'] properties
* 3: data.value must be number
