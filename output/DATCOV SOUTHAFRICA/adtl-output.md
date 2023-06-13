>adtl datcov-southafrica.toml V130\ Shortened\ Full\ Database\ _FollowUpMerge_1.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |493980 |494547 |99.885350% |
|visit          |494143 |494547 |99.918309% |
|observation    |2190779        |2190799        |99.999087% |

## subject

* 316: data must contain ['subject_id', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 251: data.age must be smaller than or equal to 120

## visit

* 404: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 20: data must contain ['phase', 'date', 'name'] properties
