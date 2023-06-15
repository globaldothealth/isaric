>adtl isaric-rapid.toml ISARICCOVID19RAPIDFo_DATA_2022-07-06_0932.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |5537   |8061   |68.688748% |
|visit          |4911   |8061   |60.922962% |
|observation    |381960 |398455 |95.860260% |

## subject

* 2271: data cannot be validated by any definition
* 249: data must contain ['age', 'pathogen', 'sex_at_birth', 'subject_id'] properties
* 2: data.age must be bigger than or equal to 0
* 2: data.age must be smaller than or equal to 120

## visit

* 3150: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 16492: data must contain ['phase', 'date', 'name'] properties
* 3: data.value must be number
