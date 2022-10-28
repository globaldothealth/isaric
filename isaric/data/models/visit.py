import datetime

from pydantic import BaseModel

from ...taxonomy import VisitDuration


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
