>adtl isaric-core.toml ISARICCOVID19COREFol_DATA_2022-08-31_1605.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |42576  |52934  |80.432236% |
|visit          |45587  |52934  |86.120452% |
|observation    |3615315        |3693324        |97.887838% |

## subject

* 10357: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 1: data.has_comorbidity_other[0] must be string

## visit

* 7347: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 77720: data must contain ['phase', 'date', 'name'] properties
* 289: data.value must be number
