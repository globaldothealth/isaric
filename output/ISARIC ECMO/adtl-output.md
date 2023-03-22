>adtl ../isaric/isaric/parsers/isaric-ecmo.toml ../../ISARIC_files/ISARIC/ISARIC\ ECMO/CoVEOT-ISARICDataOnlyLM_DATA_2023-02-03_1041.csv

|table       	|valid	|total	|percentage_valid|
|---------------|-------|-------|----------------|
|subject       	|18854	|23313	|80.873332% |
|visit         	|8948	|23313	|38.382019% |
|observation   	|1202218	|1382276	|86.973803% |

## subject

* 4459: data must contain ['subject_id', 'country_iso3', 'enrolment_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties

## visit

* 14365: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 179721: data must contain ['phase', 'date', 'name'] properties
* 337: data.value must be number
