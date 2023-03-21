>adtl ../isaric/isaric/parsers/isaric-ecmo.toml ../../ISARIC_files/ISARIC/ISARIC\ ECMO/CoVEOT-ISARICDataOnlyLM_DATA_2022-06-14_1304.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |16384  |17148  |95.544670% |
|visit          |6556   |17148  |38.231864% |
|observation    |1074931        |1239350        |86.733449% |

## subject

* 764: data must contain ['subject_id', 'country_iso3', 'enrolment_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties

## visit

* 10592: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 164098: data must contain ['phase', 'date', 'name'] properties
* 321: data.value must be number
