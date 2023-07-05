>adtl isaric-core.toml ISARICCOVID19COREFol_DATA_2022-08-31_1605.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |42770  |52934  |80.798730% |
|visit          |45422  |52934  |85.808743% |
|observation    |4001696        |4063440        |98.480499% |

## subject

* 8608: data must contain ['subject_id', 'age', 'ethnicity', 'pathogen'] properties
* 1077: data cannot be validated by any definition
* 478: data must be valid exactly by one definition (0 matches found)
* 1: data.has_comorbidity_other[0] must be string

## visit

* 7501: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 11: data.treatment_other[0] must be string

## observation

* 46427: data must contain ['phase', 'date', 'name'] properties
* 15317: data must be valid exactly by one definition (0 matches found)
