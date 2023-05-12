>adtl isaric-core.toml ISARICCOVID19COREFol_DATA_2022-08-31_1605.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |37779  |52934  |71.370008% |
|visit          |45587  |52934  |86.120452% |
|observation    |3373240        |3426826        |98.436279% |

## subject

* 15155: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties

## visit

* 7347: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 53297: data must contain ['phase', 'date', 'name'] properties
* 289: data.value must be number
