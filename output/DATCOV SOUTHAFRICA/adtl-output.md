>adtl ../isaric/isaric/parsers/datcov-southafrica.toml ../../ISARIC_files/ISARIC/DATCOV\ SA/V130\ Shortened\ Full\ Database\ _FollowUpMerge_1.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |493980 |494547 |99.885350% |
|visit          |494143 |494547 |99.918309% |
|observation    |2382966        |2382983        |99.999287% |

## subject

* 316: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 251: data.age must be smaller than or equal to 120

## visit

* 404: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 17: data must contain ['phase', 'date', 'name'] properties
