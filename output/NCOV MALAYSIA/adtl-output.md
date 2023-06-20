>adtl ncov-malaysia.toml CVPRQTA_COVID19Malaysia_DATA_2020-December.csv --encoding iso-8859-1

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |6440   |6476   |99.444101% |
|visit          |6362   |6476   |98.239654% |
|observation    |319598 |320121 |99.836624% |

## subject

* 18: data must contain ['subject_id', 'age', 'ethnicity', 'pathogen'] properties
* 15: data cannot be validated by any definition
* 3: data must be valid exactly by one definition (0 matches found)

## visit

* 114: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 421: data must be valid exactly by one definition (0 matches found)
* 102: data must contain ['phase', 'date', 'name'] properties
