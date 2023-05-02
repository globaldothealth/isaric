> adtl isaric/parsers/ccp-guinea.toml ../isaric-data/ccp-guinea/ALERRTCCPSTUDYGUINEA_DATA_2022-08-17_1038.csv --encoding=iso-8859-1

|table       	|valid	|total	|percentage_valid|
|---------------|-------|-------|----------------|
|subject       	|2720	|2741	|99.233856% |
|visit         	|2665	|2741	|97.227289% |
|observation   	|203226	|219396	|92.629765% |

## subject

* 19: data must contain ['admission_date', 'age', 'country_iso3', 'pathogen', 'sex_at_birth', 'subject_id'] properties
* 2: data.pregnancy_gestational_assessment_weeks must be number

## visit

* 76: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 16170: data must contain ['phase', 'date', 'name'] properties
