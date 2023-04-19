>adtl ../isaric/isaric/parsers/isaric-ecmo.toml ../../ISARIC_files/ISARIC/ISARIC\ ECMO/ISARIC_ECMO_Merge.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |18758  |23313  |80.461545% |
|visit          |8948   |23313  |38.382019% |
|observation    |1192046        |1372853        |86.829835% |

## subject

* 4555: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties

## visit

* 14365: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 180507: data must contain ['phase', 'date', 'name'] properties
* 300: data.value must be number
