>adtl isaric-core.toml CANSARICORE_DATA_2022-07-06_1502.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2098   |2174   |96.504140% |
|visit          |2126   |2174   |97.792088% |
|observation    |128556 |128601 |99.965008% |

## subject

* 62: data must contain ['subject_id', 'age', 'ethnicity', 'pathogen'] properties
* 8: data must be valid exactly by one definition (0 matches found) (Note: sex_at_birth missing)
* 6: data cannot be validated by any definition (Note: missing both enrolment_date and earliest_admission_date)

## visit

* 48: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 43: data must contain ['phase', 'date', 'name'] properties
* 2: data.value must be number
