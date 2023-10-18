>adtl isaric-ecmo.toml ISARIC_ECMO_Merge.csv --include-def isaric-ecmo-relsub.json

|table          |valid  |total  |percentage_valid|
|---------------|-------|-------|----------------|
|subject        |22562  |23313  |96.778621% |
|visit          |16842  |23313  |72.242955% |
|observation    |1373698        |1410093        |97.418965% |

## subject

* 687: data cannot be validated by any definition
* 64: data must be valid exactly by one definition (0 matches found)

## visit

* 6471: data must contain ['visit_id', 'subject_id', 'country_iso3', 'start_date', 'outcome', 'date_outcome'] properties

## observation

* 22143: data must contain ['phase', 'date', 'name'] properties
* 14252: data must be valid exactly by one definition (0 matches found)
