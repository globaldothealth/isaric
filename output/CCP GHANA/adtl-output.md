>adtl ccp-ghana.toml GhanaCOVID19-GaEastAndPramsoData_DATA_2022-08-04_1412-v2.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2074   |2777   |74.684912% |
|visit          |2306   |2777   |83.039251% |
|observation    |537881 |691658 |77.766902% |

## subject

* 489: data must contain ['subject_id', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 212: data.subject_id must be string
* 2: data cannot be validated by any definition

## visit

* 318: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 152: data.visit_id must be string
* 1: data.treatment_other[0] must be string

## observation

* 153775: data must contain ['phase', 'date', 'name'] properties
* 2: data.text must be string
