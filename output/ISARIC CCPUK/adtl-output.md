>adtl isaric-ccpuk.toml CCPUKSARILondon_DATA_2022-06-06_1135.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |31457  |36754  |85.587963% |
|visit          |30834  |36754  |83.892910% |
|observation    |1192364        |1202801        |99.132275% |

## subject

* 5289: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 5: data.age must be smaller than or equal to 120
* 2: data.admission_date must be date
* 1: data.age must be bigger than or equal to 0

## visit

* 5918: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 2: data.date_outcome must be date

## observation

* 10363: data must contain ['phase', 'date', 'name'] properties
* 68: data.date must be date
* 6: data.value must be number
