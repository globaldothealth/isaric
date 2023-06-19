>adtl ncov-malaysia.toml CVPRQTA_COVID19Malaysia_DATA_2020-December.csv --encoding iso-8859-1

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |6440   |6476   |99.444101% |
|visit          |6317   |6476   |97.544781% |
|observation    |320555 |320657 |99.968190% |

## subject

* 18: data must contain ['subject_id', 'age', 'ethnicity', 'pathogen'] properties
* 15: data cannot be validated by any definition
* 3: data must be valid exactly by one definition (0 matches found)

## visit

* 114: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 41: data.treatment_corticosteroid_type[0] must be one of ['Methylprednisolone', 'Prednisolone', 'Dexamethasone', 'Hydrocortisone', 'Other']
* 4: data.treatment_corticosteroid_type[1] must be one of ['Methylprednisolone', 'Prednisolone', 'Dexamethasone', 'Hydrocortisone', 'Other']

## observation

* 102: data must contain ['phase', 'date', 'name'] properties
