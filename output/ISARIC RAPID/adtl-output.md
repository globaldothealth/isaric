>adtl isaric-rapid.toml ISARICCOVID19RAPIDFo_DATA_2022-07-06_0932_temperaturefix.csv --include-defs isaric-rapid.json

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |5546   |8061   |68.800397% |
|visit          |4911   |8061   |60.922962% |
|observation    |413654 |430313 |96.128632% |

## subject

* 2510: data cannot be validated by any definition
* 2: data.age must be bigger than or equal to 0
* 2: data.age must be smaller than or equal to 120
* 1: data must be valid exactly by one definition (0 matches found)

## visit

* 3150: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 13853: data must contain ['phase', 'date', 'name'] properties
* 2806: data must be valid exactly by one definition (0 matches found)
