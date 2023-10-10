>adtl isaric-core.toml ISARICCOVID19COREFol_DATA_2022-08-31_1605.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |42760  |52934  |80.779839% |
|visit          |45422  |52934  |85.808743% |
|observation    |4226615        |4291270        |98.493336% |

## subject

* 8221: data must contain ['subject_id', 'ethnicity', 'pathogen'] properties
* 1835: data cannot be validated by any definition
* 107: data must be valid exactly by one definition (0 matches found)
* 7: data.dob_year must be bigger than or equal to 1900
* 3: data.date_of_birth must be date
* 1: data.has_comorbidity_other[0] must be string

## visit

* 7501: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 11: data.treatment_other[0] must be string

## observation

* 48052: data must contain ['phase', 'date', 'name'] properties
* 16377: data must be valid exactly by one definition (0 matches found)
* 226: data.date must be string
