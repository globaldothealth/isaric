import datetime
from enum import Enum

from ...taxonomy import Sex, Pathogen, ReferenceDateType, Ethnicity, Outcome

from pydantic import BaseModel


class Subject(BaseModel):

    # site details
    country_iso3: str
    date: datetime.date
    type_date: ReferenceDateType

    date_hospital_admission: datetime.date

    # demographics
    age: int
    sex_at_birth: Sex
    ethnicity: Ethnicity
    works_microbiology_lab: bool = None
    works_healthcare: bool = None

    # Pathogen
    pathogen: Pathogen

    # Pregnancy
    pregnancy: bool = None
    pregnancy_date_of_delivery: datetime.date
    pregnancy_birth_weight_kg: float

    # Co-morbidities
    has_chronic_hematologic_disease: bool = None
    has_asplenia: bool = None
    has_tuberculosis: bool = None
    has_dementia: bool = None
    has_obesity: bool = None
    has_rheumatologic_disorder: bool = None
    has_hiv: bool = None
    has_hypertension: bool = None
    has_malignant_neoplasm: bool = None
    has_smoking: bool = None
    has_asthma: bool = None
    has_chronic_cardiac_disease: bool = None
    has_chronic_kidney_disease: bool = None
    has_diabetes_melitus: bool = None
    has_liver_disease: bool = None
    has_apnoea: bool = None
    has_hiv_viral_suppression: bool = None
    has_inflammatory_bowel_disease: bool = None
    has_rare_disease_inborn_metabolism_error: bool = None
    has_solid_organ_transplant: bool = None
    has_tuberculosis_past: bool = None
    has_hiv_art: bool = None
    has_immunosuppression_therapy_treatment: bool = None

    # Outcome
    date_death: datetime.date = None
    outcome: Outcome
    icu_admitted: bool = None
    date_outcome: datetime.date
