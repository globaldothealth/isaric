>adtl isaric-core.toml OMS_wide_2.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2545   |2977   |85.488747% |
|visit          |2909   |2977   |97.715821% |
|observation    |301565 |301928 |99.879773% |

## subject

* 432: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties

## visit

* 68: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 359: data must contain ['phase', 'date', 'name'] properties
* 4: data.value must be number
