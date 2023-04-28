>adtl ../isaric/isaric/parsers/ccp-ghana.toml ../../ISARIC_files/ISARIC/Ghana/GhanaCOVID19-GaEastAndPramsoData_DATA_2022-08-04_1412-v2.csv

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |2049   |2777   |73.784660% |
|visit          |1952   |2777   |70.291682% |
|observation    |215005 |604004 |35.596619% |

## subject

* 516: data must contain ['subject_id', 'country_iso3', 'admission_date', 'age', 'sex_at_birth', 'ethnicity', 'pathogen'] properties
* 212: data.subject_id must be string

## visit

* 323: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 302: data.treatment_experimental_agent_type[0] must be one of ['Chloroquine', 'Hydroxychloroquine', 'Remdesivir', 'IL1 inhibitor', 'IL6 inhibitor', 'Convalescent plasma', 'Other']
* 152: data.visit_id must be string
* 34: data.treatment_experimental_agent_type[2] must be one of ['Chloroquine', 'Hydroxychloroquine', 'Remdesivir', 'IL1 inhibitor', 'IL6 inhibitor', 'Convalescent plasma', 'Other']
* 12: data.treatment_experimental_agent_type[1] must be one of ['Chloroquine', 'Hydroxychloroquine', 'Remdesivir', 'IL1 inhibitor', 'IL6 inhibitor', 'Convalescent plasma', 'Other']
* 2: data.treatment_antiviral_type[0] must be one of ['Ribavirin', 'Lopinavir/Ritonvir', 'Interferon alpha', 'Interferon beta', 'Chloroquine/Hydroxychloroquine', 'Oseltamivir (Tamiflu)', 'Zanamivir', 'Casirivimab/Imdevimab', 'Remdesivir', 'IL6 inhibitor', 'Neuraminidase inhibitor', 'Convalescent plasma', 'Anti-influenza antiviral', 'Other']

## observation

* 388998: data must contain ['phase', 'date', 'name'] properties
* 1: data.text must be string
