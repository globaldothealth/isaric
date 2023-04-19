>adtl ../isaric/isaric/parsers/isaric-rapid.toml ../../ISARIC_files/ISARIC/ISARIC\ RAPID/ISARICCOVID19RAPIDFo_DATA_2022-07-06_0932.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |5392   |8061   |66.889964% |
|visit          |4911   |8061   |60.922962% |
|observation    |366950 |390034 |94.081542% |

## subject

* 2667: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 1: data.age must be bigger than or equal to 0
* 1: data.age must be smaller than or equal to 120

## visit

* 3150: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 23081: data must contain ['phase', 'date', 'name'] properties
* 3: data.value must be number
