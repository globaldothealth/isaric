>adtl ../isaric/isaric/parsers/ccp-ghana.toml ../../ISARIC_files/ISARIC/Ghana/GhanaCOVID19-GaEastAndPramsoData_DATA_2022-08-04_1412-v2.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2350   |2777   |84.623695% |
|visit          |2301   |2777   |82.859201% |
|observation    |194491 |776981 |25.031629% |

## subject

* 217: data.subject_id must be string
* 209: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 1: data.pregnancy_gestational_assessment_weeks must be number

## visit

* 323: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 152: data.visit_id must be string
* 1: data.treatment_experimental_agent_type[1] must be one of ['Chloroquine', 'Hydroxychloroquine', 'Remdesivir', 'IL1 inhibitor', 'IL6 inhibitor', 'Convalescent plasma', 'Other']

## observation

* 582489: data must contain ['phase', 'date', 'name'] properties
* 1: data.text must be string
