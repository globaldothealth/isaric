>adtl isaric-ecmo.toml ISARIC_ECMO_Merge.csv --include-def isaric-ecmo-relsub.json

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |22567  |23313  |96.800069% |
|visit          |8944   |23313  |38.364861% |
|observation    |1241858        |1267888        |97.946980% |

## subject

* 682: data cannot be validated by any definition
* 64: data must be valid exactly by one definition (0 matches found)

## visit

* 14369: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 17846: data must contain ['phase', 'date', 'name'] properties
* 8184: data must be valid exactly by one definition (0 matches found)
