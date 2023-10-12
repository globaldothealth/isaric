> adtl isaric/parsers/idor-brazil.toml CVTDWXD_COREISARICBaseDeDado-Fechados_DATA_2022-05-25_1216.csv

|table       	|valid	|total	|percentage_valid|
|---------------|-------|-------|----------------|
|subject       	|4146	|4157	|99.735386% |
|visit         	|4123	|4157	|99.182102% |
|observation   	|202216	|204081	|99.086147% |

## subject

* 9: data cannot be validated by any definition
* 2: data must be valid exactly by one definition (0 matches found)

## visit

* 28: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties
* 5: data.treatment_corticosteroid_type[0] must be one of ['Budesonide', 'Cortisonal', 'Dexamethasone', 'Fluticasone', 'Hydrocortisone', 'Methylprednisolone', 'Mometasone', 'Prednisolone', 'Prednisone', 'Salmeterol', 'Other']
* 1: data.icu_admission_dates[0] must be date

## observation

* 1833: data must be valid exactly by one definition (0 matches found)
* 32: data must contain ['phase', 'date', 'name'] properties
