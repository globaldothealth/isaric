# A mapping guide for writing clinical data parsers

This guide contains hints and best practises to follow when writing clinical data parsers using the ISARIC model, for transformation using [adtl](https://github.com/globaldothealth/adtl). A more general overview of generic parser syntax can be found there in the [specification file](https://github.com/globaldothealth/adtl/blob/main/docs/specification.md).

## Mapping *Unknown/Not Known*

If a field contains values that specifically correspond to 'Unknown' (or semantically similar), and the field is being mapped to a **boolean** value, *do not map the unknown value*. 'Unknown' is functionally the same as an empty field; we therefore treat it in the same way. When the data is parsed, if a value is encountered which is not mapped it will be returned as `None`, in the same manner as an empty field. E.g.
```
# Values in the data: 1 (true), 0 (false), 2 (unknown), nan (empty)
[subject.has_hypertension]
  field = "hypertension"
  description = "Hypertension"
  values = {1 = true, 0 = false}
```

If mapping to a text field, you can map to 'Unknown' if desired - this may be advantageous for attributes such as ethnicity which are required and will cause a row to be flagged as invalid if data is missing.

## Date hierarchies

Date hierarchies provide a list of date fields to search through in order to provide a value. They should only be used to fill fields which are required by the schema; otherwise, if a date has not been provided, the field should remain empty.

Dates should be provided in order of most -> least specific; in general, this will inversely correspond to least -> most likely to be provided in the data. If the most specific/relevant date is also the most commonly filled field, a date hierarchy may not be appropriate. For example:

```
[adtl.defs.admissionDateHierarchy]
  combinedType = "firstNonNull"
  fields = [
    { field = "hostdat", description = "Admission date at this facility" },
    { field = "cestdat", description = "Onset date of first/earliest symptom" },
    { field = "dsstdat", description = "Date of enrolment" },
  ]
```

## combinedTypes

combinedType fields are also described in the [adtl specification file](https://github.com/globaldothealth/adtl/blob/main/docs/specification.md/#combined-type). For clinical data, it is particularly important to note the differences between `any` and `firstNonNull` and how they should be applied; they are therefore also described here.

**any**: Boolean values only. If any of the fields listed are `True`, will return `True`. If none are true but some are `False`, will return `False`; is all of the fields are `Null`, will return `None`.

**firstNonNull**: The first field in the list which is *not Null* - i.e. either True, False, or a specifc value, will be given. If *all* the fields are `None`, *the field will also be returned as `None`*.

**set**: Similar to the 'list' combinedType, `set` will return a list of items with duplicates removed. `set` should be used in place of `list` unless duplicate entries are specifically required.

## Conditional fields

Conditional fields (the `if` property within an attribute) should only be used to specifically turn 'off' an attribute.

E.g., in the following scenario, the `if` statement is redundant; if the overarching `overall_exper_cmyn` field is `None`, indicating no experimental agents were used, the sub-field `overall_exper_cmtype___4` will always also be `None`. There may also be cases where the *_cmyn housekeeping variable has been left empty but the *_cmtype fields are filled; using this `if` statement would then incorrectly filter out the information.

```
[visit.treatment_experimental_agent]
  description = "Experimental treatments used?"
  field = "overall_exper_cmyn"
  ref = "Y/N/NK"

[visit.treatment_tocilizumab]
  description = "Tocilizumab used?"
  field = "overall_exper_cmtype___4"
  values = { 0 = false, 1 = true }
  if = { overall_exper_cmyn = 1 }
```

However, below is a valid example of `if` statement usage; `dsstdtc` will usually be filled, as it is the date of discharge/outcome. However it is only valid to use it to fill a `death_date` attribute if the subject died, indicated by the `dsterm` field being equal to 4.

```
[subject.date_death]
  field = "dsstdtc"
  if = { dsterm = 4, description = "Outcome date" }

[visit.outcome]
  field = "dsterm"
  description = "Outcome date"

  [visit.outcome.values]
     1 = "discharged"
     2 = "hospitalised"
     3 = "transferred"
     4 = "death"
     5 = "discharged"

```

`if` statements controlling the observation table are automatically generated if the field is not filled in the parser, to only show the attribute if the field contains one of the mapped values, or is not an empty string for text fields.

## Phase descriptors
Phase descriptors are used within the 'observations' table to describe which time period within the study the data refers to. One of three descriptors can be used:

**pre-admission**: Specifically for medication/treatments recorded as e.g., medical history, before hospital admission. All symptoms, including those which may be described as occuring before admission, should NOT be recorded with this descriptor.

**admission**: Refers to data collected upon subject admission. Any symptoms/observations recorded at admission may refer to the day of admission, or a time-period leading up to the day of hospital admission - use the `start_date` variable in this case.

**study**: Data collected during a single hospital visit. Can refer to a single event within the visit period, or something present throughout the time spent in hospital.

**followup**: Data collected during follow-up visits. As with the 'admission' phase, the attribute can refer to the single day of the follow-up survey being completed, or to a time period between hospital discharge and the date of the follow-up form being completed.

These phases can also be used in the 'visit' table (where they are optional rather than required). For datasets where followup treatments are recorded, the 'study' and 'followup' phases can be used in the visit table to distinguish between the primary visit and any followup treatments or subsequent visits, respectively.

## Duration type

In addition to the three phase descriptors, within the observations table the `duration_type` attribute can be used to distinguish between an 'event', which denotes an observation that occurs once or multiple times within the observation period, or a 'block' to refers to something present within the entire observation period. In this case, the observation period is given by the interval between `start_date` and `date`, providing a more specific date range on top of the phase descriptors.

For example:
```
[[observation]]
  name = "headache"
  phase = "followup"
  date = { ref = "followupDateHierarchy" }
  start_date = {
    field = { ref = "followupDateHierarchy" },
    apply = { function = "startDate", params = [10] }
    }
  duration_type = "event"
  is_present = { field = "flw_headache", values = { 1 = true, 0 = false } }
  if = { flw_headache = { "!=" = 99 } }
```
records an observation of a headache which has occurred at least once in the 10 days leading up to the date of the follow-up form being completed.

## Studies with multiple data sources

Where possible, a single study should correspond to a single parser. If data has been gathered by multiple e.g., countries, there may be instances where different subsets of the data have been provided (e.g. followup data may be missed, or as the study evolves some of the fields may be deprecated). Under normal use, if *adtl* cannot find a field in the data being parsed it will stop with an error. However, for cases where a field is present in some data files but not others which use the same parser, you can tag a particular field with `can_skip`, or use a parser-wide `skipFieldPattern` variable to allow *adtl* to pass over a field without an error if it isn't found in a file.

Use this with caution - make sure that skipping over a field isn't hiding a typo or other hidden issues! Examples and further explaination can be found [here](https://github.com/globaldothealth/adtl/blob/main/docs/specification.md/#skippable-fields).

## Parser validation

There are two stages of parser validation which can be used during parser development.

### 1) During development

We recommend developing using VScode to make the most of the parser development tools. Ensure the [evenBetterToml](https://marketplace.visualstudio.com/items?itemName=tamasfe.even-better-toml) VSCode extension is present in your environment, and then add a schema comment to the top of your parser file like this:
```
#:schema ../../schemas/dev/parser.schema.json
```
The file path should be correct from the file you are developing, to the parser.schema.json file. If you have not changed the structure of the repository and are writing a file within the `isaric/parsers/` folder, this path should be correct.

Once this is set up, some autocompletion of code and hints will be availbe to help write your parser file, with error highlighting included.

### 2) Testing the parser

Once the parser file has been written, it can be validated (i.e. check what percentage of the data generated using this parser is valid according to the schemas) using [adtl](https://github.com/globaldothealth/adtl). You should ensure your parser file contains a table which looks similar to the following, with the `schema` key included:
```
[adtl.tables]
    study = { kind = "constant" }
    subject = { kind = "groupBy", groupBy = "subject_id", aggregation = "lastNotNull", schema = "../../schemas/dev/subject.schema.json" }
    visit = { kind = "groupBy", groupBy = "visit_id", aggregation = "lastNotNull", schema = "../../schemas/dev/visit.schema.json" }
    observation = { kind = "oneToMany", schema = "../../schemas/dev/observation.schema.json", common = { visit_id = { field = "\ufeffsubjid", sensitive = true } } }
```
The schema file path should, as above, match the path from your parser file, to the relevant schema file. If you only wish to validate a subset of the tables (e.g. only the subject table has been written so far) the other tables should be commented out.

Follow the instructions on [adtl](https://github.com/globaldothealth/adtl) for running the data transformation; the terminal command should follow the format
```
adtl specification-file input-file
```
Once the command has run, adtl will generate a report in the terminal showing validation error counts, and will prodice error messages indicating what is causing the parser validation to fail at particular steps.

Each output file will also contain two additional columns, `adtl_valid` and `adtl_error`, with data indicating whether the output row is valid according to the schema (True, empty, respectively) or invalid (False, error message).

### Check for missing data

You can check how many of the attribute options listed in the schema have been included in the parser by running the `missing_fields.py` script. From the root of the repository:
```
python3 scripts/checkfields/missing_fields.py isaric/parsers/<your parser name>
```
will check a single parser, while
```
python3 scripts/checkfields/missing_fields.py isaric/parsers --all
```
will test all the parsers in the file.

A terminal output will list the percentage coverage of each table, and the script produces a `check_fields.csv` file listing each of the schema attributes and marking them as True (present) of False (absent) for each parser being tested. The aim should be to have every possible attribute present where there is data from the study (i.e. higher coverage).

# Table-by-table notes for each attribute

Listed below are all the attributes for the Subject, Visit and Observation tables, grouped by table (and where appropriate, supersets), with notes on how they should be applied.

General notes on naming conventions:
 * **has_** indicates a comorbidity. In all cases, listed comorbidities should be clinically diagnosed to be recorded.
 * **treatment_** indicates a treatment administered during a visit
 * **_type** indicates an attribute containing lists of specific drug names
 * **_other** is used for fields containing free text

## Subject

**subject_id**: Text. Unique ID for the subject (NOTE: currently this is the same as the visit ID, prior to implementation of RELSUB matching).

**dataset_id**: Text. Refers to the specifc ID/Version of the dataset being used (NOTE TO DEVS: should this be study metadata instead?)

**country_iso3**: Text. Alpha-3 country code of the <ins>study site. </ins> NOTE TO DEVS: If this relates to study site only, it shouldn't be in the subject table.

**enrolment_date**: Date. Date of subject enrolement into the study.

**admission_date**: Date. Date of admission to site NOTE TO DEVS: Move this to visit & combine with start_date?

**age**: Value. Age of the subject in years.

**sex_at_birth**: Text. One of
  * male
  * female
  * intersex
  * non-binary NOTE TO DEVS - this isn't a sex at birth, rather current sex/gender. suggest remove, or create new attribute for gender/similar? Or rename to just 'sex'.

**ethnicity**: Text. Subject's ethnicity.

<a name="pathogen"></a>**pathogen**: Text. Pathogen subject is being studied for.

**pregnancy**: Bool. Is the subject currently pregnant?

**preganacy_date_of_delivery**: Date. If the subject gave birth during the study period, give the date

**pregnancy_birth_weight_kg**: Value. Weight of infant at birth, kg.

**pregancy_outcome**: Text. Outcome of the pregnancy, one of:
  * live_birth
  * still_birth

**pregnancy_gestational_outcome**: Text: One of
  * term_birth
  * preterm_birth

**pregnancy_whether_breastfed**: Bool. Is the subject currently breastfeeding/ did they breastfeed during the study period?

**pregnancy_post_partum**: Bool. Is the subject post-partum (up to 6 weeks post-delivery) at the point of enrolement?

**pregnancy_gestational_outcome_weeks**: Value. Gestational age assesment at point of enrolement. NOTE TO DEVS: This is how the attribute has been used, but the name is confusing; suggest rename to gestational_age_weeks/redefine this to be the number of weeks at which subject gave birth?

**has_asplenia**: Bool. Does the subject have asplenia?

**has_tuberculosis** Bool. Does the subject currently have tuberculosis?

**has_tuberculosis_past** Bool. Has the subject had TB in the past?

**has_dementia** Bool. Does the subject have dementia?

**has_obesity** Bool. Is the subject obese?

**has_rheumatologic_disorder** Bool. Does the subject have a rheumatologic disorder?

**has_hiv**: Bool. Does the subject have HIV?

**has_hiv_art** Bool. Is the subject being treated for HIV using ART?

**has_hypertension**: Bool. Does the subject have hypertension?

**has_malignant_neoplasm**: Bool. Does the subject have a malignant neoplasm (cancerous tumor)?

**has_malnutrition**: Bool. Is the subject malnourished?

**has_smoking**: Text. Smoking history. One of
  * current
  * former
  * never

**has_asthma**: Bool. Does the subject have asthma?

**has_chronic_cardiac_disease**: Bool. Does the subject have a chronic cardiac disease?

**has_chronic_kidney_disease**: Bool. Does the subject have a chronic kidney disease?

**has_diabetes**: Bool. Does the subject have diabetes?

**diabetes_type**: Text. Type of diabetes; one of
  * type-1
  * type-2
  * gestational

**has_liver_disease**: Bool. Does the subject have liver disease? (Note - this usually combines mild + moderate liver diease)

**has_apnoea**: Bool. Does the subject have apnoea?

**has_inflamatory_bowel_disease** Bool. Does the subject have inflamatory bowel disease?

**has_rare_disease_inborn_metabolism_error** Bool. Does the subject have a rare inborn disease?

**has_solid_organ_transplant** Bool. Has the subject undergone a solid organ transplant? (Note - include bone marrow transplants here)

<a name="immunosuppressed"></a>**has_immunosuppression_therapy** Bool. Is the subject chronically immunosuppressed?

**has_comorbidity_other**: Set. Any other comorbidity - free text field.

**has_died**: Bool. Has the subject died since being enroled in the study? Can take data from both hospitalisation and follow-up surveys, and includes non-covid related deaths where specified (as in many studies the cause of death is unknown).

**date_death**: Date. Takes date from outcome date/date of death (if outcome records death)/death reported at followup.

**icu_admitted**: Bool. Has the subject been admitted to ICU at any time since study enrolment?

## Visit
Contains data specific to the visit, including details on which treatments the subject recieved.

### Superset, general level indicators:

**treatment_oxygen_therapy**: Indicates at least one type of oxygen therapy and/or respiratory support has been administered. Subsets (all boolean indicators) are:
+ *treatment_oxygen_mask_unspecified* - NOTE TO DEVS: needs to be added. Captures O2 therapy delivered by any method other than a HFNC - e.g., standard mask or cannula.
+ *treatment_high_flow_nasal_cannula*
+ *treatment_noninvasive_ventilation* - Ventilation via e.g., BIPAP/CPAP mask
+ *treatment_invasive_ventilation* - Intubation. Includes deprecated 'mechanical_support' attribute
+ *treatment_prone_positioning* - Note, only if field is labelled as prone <ins>ventilation. </ins>
+ *treatment_ecmo*

### General drug types
The general drug categories *antiviral*, *antibiotic*, *corticosteroid* and *experimental_agent* all have a set of three hierarchical attributes, e.g. for antivirals:
+ **treatment_antiviral**: Bool. If antivirals have been administered during the visit
+ **treatment_antiviral_type**: Set. Lists all the different types of antiviral administered. Should only be used where values are mapped, as there is a restricted list of accepted values defined in the schema - i.e. do not map a free text field here.
+ **treatment_antiviral_type_other**: Set. For free text fields listing the names of antivirals used.

### other fields

**visit_id**: Text. Unique ID for the specific visit.

**subject_id**: Text. Unique ID for the subject (NOTE: currently this is the same as the visit ID, prior to implementation of RELSUB matching).

**dataset_id**: Text. Refers to the specifc ID/Version of the dataset being used (NOTE TO DEVS: should this be study metadata instead?)

**country_iso3**: Text. Alpha-3 country code of the <ins>study site. </ins>

**start_date**: Date. Start date of the visit - usually date of admission to hospital.

**pathogen_test_date**: Date. Date of test (date done, not date of result) for the pathogen specified in the [subject table](pathogen).

**icu_admission**: Bool. Admitted to ICU in this visit?

**icu_admission_dates**: List: List of admission date(s) to ICU.

**treatment_dialysis**: Bool. Did the subject recieve dialysis during this visit?

**treatment_inotropes_vasopressors**: Bool. Treatment with vasopressors during this visit?

**treatment_antifungal_agent**: Bool. Treatment with a antifungal agent(s)?

**treatment_anticoagulation**: Bool. Treated with anticoagulants during the visit? (Note - this is often combines a general anticoagulation field with those specific to Heparin. NOTE TO DEVS: merge (if not already) wih treatment_indication_anticoagulation)

**treatment_inhaled_nitric_oxide**: Bool. Treated with nitric oxide inhalation?

**treatment_ace_inhibitors**: Bool. Treated with ACE inhibitors?

**treatment_arb**: Bool. Treated with ARB's?

**treatment_antimalarial**: Bool. Treated with antimalarials?

**treatment_immunosuppressant**: Bool. Treated with immunosuppresants? (Note - this is specific to this visit. If the subject was on immunosuppresants for a chronic condition prior to admission, this should be recorded under [has_immunosuppression_therapy](immunosuppressed) in the subject table as a comorbidity.)

**treatment_intravenous_fluids**: Bool. Did the subject recieve IV fluids during the visit?

**treatment_nsaid**: Bool. Was the subject treated with non-steroidal meds during the visit?

**treatment_neuromuscular_blocking_agents**: Bool. Was the subject treated with neuromuscular blocking agents during the visit?

**treatment_cpr**: Bool. Did the subject recieve CPR?

**treatment_offlabel**: Bool. Was the subject treated with off-label medications, e.g. for compassionate use?

**treatment_cardiovascular**: Bool. Did the subject recieve cardiovascular support, e.g., Pacing, Intropic support, mechanical (e.g. ecmo, intra-aeortic balloon pump), cpr. NOTE TO DEVS: Consider making this a superset in the same manner as oxygen_therapy

**treatment_colchine**: Bool. Was the pateint treated with Colchine?

**treatment_immunoglobulins**: Bool. Did the subject recieve immunoglobulins?

**treatment_delirium** - NOTE TO DEVS do we still have this? delirium is an observation ( I think this comes from the traffic light doc's `medication for delirium` - but this only occurs in one study.)

**treatment_monoclonal_antibody**: Bool. Was the subject treated with monoclonal antibodies?

**treatment_other**: Set. Any other treatments, or treatments recorded as free text fields, should be recorded here.

**treatment_pacing**: Bool. Did the subject recieve heart pacing during the visit?

**outcome** Text. Outcome of the visit, one of:
  + death
  + hospitalised
  + transferred
  + recovered
  + discharged
  + palliative discharge

**date_outcome** Date. Date the visit outcome was recorded; either date of death, or date the subject left this facility.

## Observation
Complications should be recorded here, not in the subject table.

### Superset, general level indicators:

**cough**: Indicates any type of cough. Subsets are
+ *cough_dry*
+ *cough_with_sputum_production* (wet cough)
+ *cough_with_haemoptysis* (bloody cough)

Should be a combinedType = "any", listing all the cough fields for the corresponding phase (admission, study etc). If individual dates are given for each cough type, they should be combined with `min`, to give the earliest date a cough presented. Should then also be broken down into the subtypes for the phase. For example:
```
[[observation]]
  name = "cough"
  phase = "admission"
  date = { ref = "admissionDateHierarchy" }
  duration_type = "event"

  [observation.start_date]
    combinedType = "min"
    fields = [
      { field = "dry_cough_date" },
      { field = "wet_cough_date" },
      { field = "blood_cough_date" },
    ]

  [observation.is_present]
    combinedType = "any"
    fields = [
      { field = "cough", description = "Cough", ref = "Y/N/NK" },
      { field = "dry_cough", description = "Dry cough", ref = "Y/N/NK" },
      { field = "wet_cough", description = "Wet cough", ref = "Y/N/NK" },
      { field = "blood_cough", description = "Blood cough", ref = "Y/N/NK" },
    ]
```

### Other fields

**avpu**: Text. Where is the subject on the AVPU conciousness scale (Alert, Voice, Pain, Unresponsive)

**abdominal_pain**: Bool.

**altered_conciousness_confusion**: Bool. If field only records confusion, not altered conciousness, use [confusion](confusion)

**anorexia**: Bool.

**base_excess**: Value. Difference between observed and normal buffer base concentration for oxygenated blood.

**bleeding**: Bool. For bleeding (other) observations. If field is described as bleeding (haemorrhage) or similar, use *bleeding_haemorrhage*.

**bleeding_haemorrhage**: Bool.

**chest_pain**: Bool.

**clinical_classification_critical_illness_scale**: Currently Unused. Traffic-light suggests only in one parser, suggest editing or removal.

**clinical_classification_pneumonia_needing_oxygen**: Bool. NOTE TO DEVS - Only used once (guinea), only one according to traffic light doc - suggest edit to just pneumonia complication, with context for viral/bacterial.

**clinical_frailty_score**: Value. [Frailty scale](https://www.bgs.org.uk/sites/default/files/content/attachment/2018-07-05/rockwood_cfs.pdf)

<a name="confusion"></a> **confusion**: Bool.

**conjunctavitis**: Bool.

**cyanosis**: Bool. Presence of cyanosis (blue/purple hue to skin)

**diarrhoea**: Bool.

**diastolic_blood_pressure_mmHg**: Value.

**systolic_blood_pressure_mmHg**: Value.

**mean_arterial_blood_pressure_mmHg**: Value.

**ear_pain**: Bool.

**fatigue_malaise**: Bool.

**feeding_intolerence_peadiatrics** Bool. Unused.

**glasgow_coma_score**: Value. [Coma scale](https://www.glasgowcomascale.org)

**headache**: Bool.

**heart_rate_bmp**: Value.

**heart_sounds**: Bool.

**hepatomegaly** Bool. Enlarged liver? (Unused)

**history_of_fever** Bool. Recently feverish? For admission/followup where the subject self-reports.

<a name="inability_to_walk"></a> **inability_to_walk**: boolean indicator. Where a relevant field contains a scale, rather than boolean Y/N responses, use [inability_to_walk_scale](inability_to_walk_scale).

<a name="inability_to_walk_scale"></a>**inability_to_walk_scale**: Use a 1-4 scale to indicate the degree of difficulty a subject has walking. Values should map to: *1-No difficulty, 2-Some difficulty, 3-Lots of difficulty, 4-Unable to walk*. If the field contains a greater number of options, they should be mapped onto a 1-4 scale, rounding down. E.g., for a 1-5 scale of: *1-no inability, 2-slight inability, 3-moderate inability, 4-severe inability, 5-unable*, option 3 (moderate inability) should be rounded down and mapped to *2-some difficulty* in the 1-4 scale. If a relevant field instead contains a boolean Y/N response, use [inability_to_walk](#inability_to_walk) instead.

**irritability_peadiatrics**: Bool. Unused.

**joint_pain**: Bool.

**loss_of_smell**: Bool. If loss of smell/taste, use combined attribute below.

**loss_of_smell_or_taste**: Bool. For where smell/taste loss is combined.

**loss_of_taste**: Bool.

**lower_chest_wall_indrawing**: Bool.

**lung_sounds**: Bool. Unused.

**lymphadenopathy**: Bool. Combines adenopathy and lymphadenopathy.

**mid_upper_arm_circumference_cm**: Value.

**muscle_aches**: Bool.

**other_symptom**: Set (Text). List any other symptoms, or free text fields describing symptoms, here.

**oxygen_o2hb**: Unused, not sure what it relates to.

**oxygen_flow_volume_max**: Value. If the subject recieved O2 therapy, record the maximum flow volume.

**oxygen_saturation_percent**: Value. Use context to note whether observation was made on room air, on while on oxygen.

**pao2**: Value. Use context to record whether this is an arterial, venous or capillary measurement if data is provided. NOTE TO DEVS - We should pick/ consult on a default unit for pao2/pco2.

**pco2**: Value. Use context to note if this is from the same blood gas record as the *pao2*/*pH* observation.

**pH**: Value. Use context to note if this is from the same blood gas record as the *pao2*/*pco2* observation.

**respiratory_rate**: Value.

**richmond_agitation-sedation_scale**: Value.

**riker_sedation-agitation_scale**: Value.

**runny_nose**: Bool.

**seizures**: Bool.

**severe_dehydration**: Bool. Clinically diagnosed only.

**shortness_of_breath**: Bool.

**skin_rash**: Bool.

**skin_ulcers**: Bool.

**sore_throat**: Bool.

**sternal_capillary_refill_time_greater_2s**: Bool. May need to use conditional statements if the refill time is given rather than a yes/no response.

**temperature_celsius**: Value

**time_of_admission**: Text (date). NOTE TO DEVS - Does this belong in the observations/complications table? Better in the visit table?

**total_fluid_output_ml**: Value.

**transfer_from_another_facility**: Bool. NOTE TO DEVS - Does this belong in the observations/complications table? Better in the visit table?

**vomiting_nausea**: Bool.

**wheezing**: Bool.