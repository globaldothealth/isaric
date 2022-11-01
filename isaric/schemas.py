import datetime

from pydantic import BaseModel, validator

from ..taxonomy import (
    Diabetes,
    Ethnicity,
    Observation,
    Outcome,
    Pathogen,
    PregnancyGestationalOutcome,
    ReferenceDateType,
    Sex,
    Smoker,
    VisitDuration,
)


class Study(BaseModel):

    id: int
    name: str
    date: datetime.datetime
    end_date: datetime.datetime = None
    location: dict[str]  # GeoJSON
    country_iso3: str
    description: str


class Subject(BaseModel):

    id: int
    study_id: int

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
    pregnancy_outcome: str = None
    pregnancy_gestational_outcome: PregnancyGestationalOutcome = None
    pregnancy_whether_breastfed: bool = None
    pregnancy_post_partum: bool = None
    pregnancy_gestational_assessment_days: int = None

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
    has_smoking: Smoker = None
    has_asthma: bool = None
    has_chronic_cardiac_disease: bool = None
    has_chronic_kidney_disease: bool = None
    has_diabetes: bool = None
    diabetes_type: Diabetes = None
    has_liver_disease: bool = None
    has_apnoea: bool = None
    has_hiv_viral_suppression: bool = None
    has_inflammatory_bowel_disease: bool = None
    has_rare_disease_inborn_metabolism_error: bool = None
    has_solid_organ_transplant: bool = None
    has_tuberculosis_past: bool = None
    has_hiv_art: bool = None
    has_immunosuppression_therapy_treatment: bool = None
    has_comorbidity_other: list[str] = []

    hiv_latest_cd4: tuple[int, int]
    hiv_latest_viral_load_copies_per_ml: int = None

    @validator("hiv_latest_cd4")
    def is_valid_range(cls, v):
        assert v[0] > 0 and v[1] > 0 and v[0] <= v[1]
        return v

    # Outcome
    date_death: datetime.date = None
    outcome: Outcome
    icu_admitted: bool = None
    date_outcome: datetime.date


class Visit(BaseModel):

    id: int
    # site details
    country_iso3: str
    subject_id: int
    study_id: int
    start_date: datetime.date
    end_date: datetime.date
    duration_type: VisitDuration

    pathogen_test_date: datetime.date = None
    icu_admission: bool = None
    icu_discharge_date: datetime.date = None
    icu_admission_date: datetime.date = None

    treatment_dialysis: bool = None
    treatment_inotropes_vasopressors: bool = None
    treatment_ecmo: bool = None
    treatment_corticosteroid: bool = None
    treatment_oxygen_therapy: bool = None
    treatment_prone_position: bool = None
    treatment_invasive_ventilation: bool = None
    treatment_antifungal_agent: bool = None
    treatment_antivirals: bool = None
    treatment_antibiotics: bool = None
    treatment_anticoagulation: bool = None
    treatment_experimental_agent: bool = None
    treatment_inhaled_nitric_oxide: bool = None
    treatment_noninvasive_ventilation: bool = None
    treatment_ace_inhibitors: bool = None
    treatment_arb: bool = None
    treatment_antimalarial: bool = None
    treatment_dexamethasone: bool = None
    treatment_nonsteroidal: bool = None
    treatment_high_flow_nasal_cannula: bool = None
    treatment_steroids: bool = None
    treatment_immunosuppressant: bool = None
    treatment_intravenous_fluids: bool = None
    treatment_nsaid: bool = None
    treatment_neuraminidase: bool = None
    treatment_oxygen_interface: bool = None
    treatment_cpr: bool = None
    treatment_offlabel: bool = None
    treatment_respiratory_support: bool = None
    treatment_tocilizumab: bool = None
    treatment_indication_anticoagulation: bool = None
    treatment_cardiovascular: bool = None
    treatment_colchicine: bool = None
    treatment_immunoglobulins: bool = None
    treatment_delirium: bool = None
    treatment_monoclonal_antibody: bool = None
    treatment_other: list[str] = []

    treatment_oxygen_mechanical_support: bool = None
    treatment_oxygen_therapy: bool = None
    treatment_pacing: bool = None

    treatment_o2_flow_vol_max: int = None


class Observation(BaseModel):

    id: int
    visit_id: int
    subject_id: int
    study_id: int

    date: datetime.datetime
    end_date: datetime.datetime = None
    value_num: float = None
    value_char: str = None
    is_present: bool = None
    name: Observation
