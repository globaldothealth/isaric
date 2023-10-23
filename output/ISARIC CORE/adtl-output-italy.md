>adtl isaric-core.toml OMS_wide_2.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2559   |2977   |85.959019% |
|visit          |2908   |2977   |97.682230% |
|observation    |322690 |373517 |86.392319% |

## subject

* 408: data must contain ['subject_id', 'ethnicity', 'pathogen'] properties
* 10: data cannot be validated by any definition

## visit

* 69: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 50369: data must contain ['phase', 'date', 'name'] properties
* 458: data must be valid exactly by one definition (0 matches found)
