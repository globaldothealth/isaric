> adtl isaric/parsers/ccp-guinea.toml ../isaric-data/ccp-guinea/ALERRTCCPSTUDYGUINEA_DATA_2022-08-17_1038.csv --encoding=iso-8859-1

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2724   |2741   |99.379788% |
|visit          |2665   |2741   |97.227289% |
|observation    |203299 |219579 |92.585812% |

## subject

* 15: data must contain ['age', 'pathogen', 'sex_at_birth', 'subject_id'] properties
* 2: data.pregnancy_gestational_age_weeks must be number

## visit

* 76: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 16280: data must contain ['phase', 'date', 'name'] properties
