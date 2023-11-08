> adtl isaric/parsers/isaric-ccpuk.toml ../isaric-data/isaric-ccpuk/CCPUKSARILondon_DATA_2022-06-06_1135.csv --include-def isaric/parsers/relsub.json

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |31619  |36754  |86.028732% |
|visit          |30810  |36754  |83.827611% |
|observation    |1414376        |1427543        |99.077646% |

## subject

* 4153: data cannot be validated by any definition
* 944: data must contain ['subject_id', 'ethnicity', 'pathogen'] properties
* 30: data must be valid exactly by one definition (0 matches found)
* 5: data.age must be smaller than or equal to 120
* 2: data.earliest_admission_date must be date
* 1: data.age must be bigger than or equal to 0

## visit

* 5939: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 2: data.date_outcome must be date
* 2: data.start_date must be date
* 1: data.pathogen_test_date must be date

## observation

* 10814: data must be valid exactly by one definition (0 matches found)
* 2279: data must contain ['phase', 'date', 'name'] properties
* 74: data.date cannot be validated by any definition
