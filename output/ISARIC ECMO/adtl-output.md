>adtl isaric-ecmo.toml ISARIC_ECMO_Merge.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |22567  |23313  |96.800069% |
|visit          |8944   |23313  |38.364861% |
|observation    |1153536        |1319487        |87.423067% |

## subject

* 440: data cannot be validated by any definition
* 306: data must contain ['age', 'pathogen', 'sex_at_birth', 'subject_id'] properties

## visit

* 14369: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 165736: data must contain ['phase', 'date', 'name'] properties
* 215: data.value must be number
