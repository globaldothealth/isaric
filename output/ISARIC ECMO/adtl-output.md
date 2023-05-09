>adtl ../isaric/isaric/parsers/isaric-ecmo.toml ../../ISARIC_files/ISARIC/ISARIC\ ECMO/ISARIC_ECMO_Merge.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |18905  |23313  |81.092095% |
|visit          |8944   |23313  |38.364861% |
|observation    |1152489        |1303066        |88.444407% |

## subject

* 4408: data must contain ['admission_date', 'age', 'country_iso3', 'pathogen', 'sex_at_birth', 'subject_id'] properties

## visit

* 14369: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 150362: data must contain ['phase', 'date', 'name'] properties
* 215: data.value must be number
