>adtl ../isaric/isaric/parsers/ccp-ghana.toml ../../ISARIC_files/ISARIC/Ghana/GhanaCOVID19-GaEastAndPramsoData_DATA_2022-08-04_1412-v2.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2049   |2777   |73.784660% |
|visit          |2306   |2777   |83.039251% |
|observation    |459059 |604004 |76.002642% |

## subject

* 516: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 212: data.subject_id must be string

## visit

* 318: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 152: data.visit_id must be string
* 1: data.treatment_other[0] must be string

## observation

* 144943: data must contain ['phase', 'date', 'name'] properties
* 2: data.text must be string
