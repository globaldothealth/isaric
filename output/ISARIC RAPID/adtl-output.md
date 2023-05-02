>adtl ../isaric/isaric/parsers/isaric-rapid.toml ../../ISARIC_files/ISARIC/ISARIC\ RAPID/ISARICCOVID19RAPIDFo_DATA_2022-07-06_0932.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |5399   |8061   |66.976802% |
|visit          |4911   |8061   |60.922962% |
|observation    |373176 |394863 |94.507715% |

## subject

* 2660: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 1: data.age must be bigger than or equal to 0
* 1: data.age must be smaller than or equal to 120

## visit

* 3150: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 21684: data must contain ['phase', 'date', 'name'] properties
* 3: data.value must be number
