import datetime
from typing import Any

from pydantic import BaseModel

from .pydantic_types import IntegerRange, DateRange, PositiveInt

from .taxonomy import (
    Diabetes,
    Ethnicity,
    ObservationName,
    Outcome,
    Pathogen,
    PregnancyGestationalOutcome,
    ReferenceDate,
    Sex,
    Smoker,
    VisitDuration,
)


class Study(BaseModel):
    study_id: str
    study_version: PositiveInt
    name: str
    date: datetime.datetime
    end_date: datetime.datetime | None = None
    location: dict[str, Any] | None = None  # GeoJSON
    country_iso3: str
    description: str


class Subject(BaseModel):
    subject_id: str
    study_id: str
    study_version: PositiveInt

    # site details
    country_iso3: str
    enrolment_date: datetime.date
    admission_date: datetime.date | None = None

    # demographics
    age_years: PositiveInt
    sex_at_birth: Sex
    ethnicity: Ethnicity
    works_microbiology_lab: bool | None = None
    works_healthcare: bool | None = None

    # Pathogen
    pathogen: Pathogen

    # Pregnancy
    pregnancy: bool | None = None
    pregnancy_date_of_delivery: datetime.date | None = None
    pregnancy_birth_weight_kg: float
    pregnancy_outcome: str | None = None
    pregnancy_gestational_outcome: PregnancyGestationalOutcome = None
    pregnancy_whether_breastfed: bool | None = None
    pregnancy_post_partum: bool | None = None
    pregnancy_gestational_assessment_weeks: float | None = None

    # Co-morbidities
    has_chronic_hematologic_disease: bool | None = None
    has_asplenia: bool | None = None
    has_tuberculosis: bool | None = None
    has_dementia: bool | None = None
    has_obesity: bool | None = None
    has_rheumatologic_disorder: bool | None = None
    has_hiv: bool | None = None
    has_hypertension: bool | None = None
    has_malignant_neoplasm: bool | None = None
    has_smoking: Smoker | None = None
    has_asthma: bool | None = None
    has_chronic_cardiac_disease: bool | None = None
    has_chronic_kidney_disease: bool | None = None
    has_diabetes: bool | None = None
    diabetes_type: Diabetes = None
    has_liver_disease: bool | None = None
    has_apnoea: bool | None = None
    has_hiv_viral_suppression: bool | None = None
    has_inflammatory_bowel_disease: bool | None = None
    has_rare_disease_inborn_metabolism_error: bool | None = None
    has_solid_organ_transplant: bool | None = None
    has_tuberculosis_past: bool | None = None
    has_hiv_art: bool | None = None
    has_immunosuppression_therapy_treatment: bool | None = None
    has_comorbidity_other: list[str] = []

    hiv_latest_cd4: IntegerRange
    hiv_latest_viral_load_copies_per_ml: int | None = None

    has_died: bool | None = None
    date_death: datetime.date | None = None
    icu_admitted: bool | None = None


class Visit(BaseModel):
    visit_id: str
    # site details
    country_iso3: str
    subject_id: int
    study_id: str
    study_version: PositiveInt
    start_date: datetime.date
    end_date: datetime.date
    duration_type: VisitDuration = VisitDuration.admission

    pathogen_test_date: datetime.date | None = None
    icu_admission: bool | None = None

    # Multiple ICU admissions are possible
    icu_admission_dates: list[DateRange] | None = None

    treatment_dialysis: bool | None = None
    treatment_inotropes_vasopressors: bool | None = None
    treatment_ecmo: bool | None = None
    treatment_corticosteroid: bool | None = None
    treatment_oxygen_therapy: bool | None = None
    treatment_prone_position: bool | None = None
    treatment_invasive_ventilation: bool | None = None
    treatment_antifungal_agent: bool | None = None
    treatment_antivirals: bool | None = None
    treatment_antibiotics: bool | None = None
    treatment_anticoagulation: bool | None = None
    treatment_experimental_agent: bool | None = None
    treatment_inhaled_nitric_oxide: bool | None = None
    treatment_noninvasive_ventilation: bool | None = None
    treatment_ace_inhibitors: bool | None = None
    treatment_arb: bool | None = None
    treatment_antimalarial: bool | None = None
    treatment_dexamethasone: bool | None = None
    treatment_high_flow_nasal_cannula: bool | None = None
    treatment_steroids: bool | None = None
    treatment_immunosuppressant: bool | None = None
    treatment_intravenous_fluids: bool | None = None
    treatment_nsaid: bool | None = None
    treatment_neuraminidase: bool | None = None
    treatment_cpr: bool | None = None
    treatment_offlabel: bool | None = None
    treatment_tocilizumab: bool | None = None
    treatment_indication_anticoagulation: bool | None = None
    treatment_cardiovascular: bool | None = None
    treatment_colchicine: bool | None = None
    treatment_immunoglobulins: bool | None = None
    treatment_delirium: bool | None = None
    treatment_monoclonal_antibody: bool | None = None
    treatment_other: list[str] = []

    treatment_pacing: bool | None = None

    treatment_o2_flow_vol_max: int | None = None

    outcome: Outcome
    date_outcome: datetime.date


class Observation(BaseModel):
    observation_id: int
    visit_id: str
    subject_id: str
    study_id: str
    study_version: PositiveInt

    date: datetime.datetime
    end_date: datetime.datetime | None = None
    value_num: float | None = None
    value_char: str | None = None
    is_present: bool | None = None
    name: ObservationName
