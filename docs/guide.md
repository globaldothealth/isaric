# A mapping guide for writing clinical data parsers

This guide contains hints and best practises to follow when writing clinical data parsers using the ISARIC model, for transformation using [adtl](https://github.com/globaldothealth/adtl). A more general overview of generic parser syntax can be found there.

## Date hierarchies

Date hierarchies provide a list of date fields to search through in order to provide a value. They should only be used to fill fields which are required by the schema; otherwise, if a date has not been provided, the field should remain empty.

Dates should be provided in order of most -> least specific; in general, this will inversely correspond to least -> most likely to be provided in the data. If the most specific/relevant date is also the most commonly filled field, a date hierarchy may not be appropriate.

TODO: Examples?

## combinedTypes

combinedType fields are also described in the [adtl specification file](https://github.com/globaldothealth/adtl/blob/main/docs/specification.md). For ISARIC, it is particularly important to note the differences between `any` and `firstNonNull` and how they should be applied; they are therefore also described here.

**any**: If any of the fields listed are non-null (truthy), the attribute will be set to `True`. Otherwise, it will be set to `False`; *even if all the fields given as options are `None`*.

**firstNonNull**: The first field in the list which is *not Null* - i.e. either True, False, or a specifc value, will be given. If *all* the fields are `None`, *the field will also be returned as `None`* (**Note to devs - This is still an open issue, this is the desired behavior rather than current**).

If it is important that an attribute distinguishes between `True/False` and `None` (e.g., there is an important distinction between an observation which has been made and where the condition is either present or absent, and an observation not being made at all), then 'firstNonNull' should be used rather than 'any'.

## Conditional fields

Conditional fields (the `if` property within an attribute) should only be used to specifically turn 'off' an attribute.

E.g., in the following scenario, the `if` statement is redundant; if the overarching `overall_exper_cmyn` field is `None`, indicating no experimental agents were used, the sub-field `overall_exper_cmtype___4` will always also be `None`.

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

However, below is a valid example of `if` statement usage; `dsstdtc` will usually be filled, as it is the date of discharge/outcome. However it is only valid to use it to fill a `death_date` attribute if the patient died, indicated by the `dsterm` field being equal to 4.

```
[subject.date_death]
  field = "dsstdtc"
  if = { dsterm = 4, description = "Outcome date" }

[visit.outcome]
  field = "dsterm"
  description = "Outcome date"
  values = {
    1 = "discharged"
    2 = "hospitalised"
    3 = "transferred"
    4 = "death"
    5 = "discharged"
  }
```

## Phase descriptors
Phase descriptors are used within the 'visit' and 'observations' tables to describe which time period within the study the data refers to. One of three descriptors can be used:

**admission**: Refers to data collected upon patient admission; general patient data (age, gender etc) plus any co-morbidities. Any symptoms/observations recorded at admission may refer to the day of admission, or a time-period leading up to the day of hospital admission.

**study**: Data collected during a single hospital visit. Can refer to a single event within the visit period, or something present throughout the time spent in hospital.

**follow-up**: Data collected during follow-up visits. As with the 'admission' phase, the attribute can refer to the single day of the follow-up survey being completed, or to a time period between hospital discharge and the date of the follow-up form being completed.

In addition to the three phase descriptors, within the observations table the `duration_type` attribute can be used to distinguish between an 'event', which denotes an observation that occurs once or multiple times within the observation period, or a 'block' to refers to something present within the entire observation period. In this case, the observation period is given by the interval between `start_date` and `date`, providing a more specific date range on top of the phase descriptors.
