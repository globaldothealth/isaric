>adtl ccp-drc.toml CVDSVGZ_ALERRT22062022_DATA_2022-08-19_0838.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |124    |126    |98.412698% |
|visit          |121    |126    |96.031746% |
|observation    |15746  |16156  |97.462243% |

## subject

* 1: data must be valid exactly by one definition (0 matches found)
* 1: data must contain ['subject_id', 'age', 'ethnicity', 'pathogen'] properties

## visit

* 4: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 1: data.treatment_other[0] must be string

## observation

* 410: data must contain ['phase', 'date', 'name'] properties
