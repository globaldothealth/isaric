"""
Export G.h-ISARIC schema to FHIR resources
"""

import sys
import csv
import json
import uuid
from dataclasses import dataclass
from typing import Optional, Literal, Any


@dataclass
class Patient:
    id: str
    gender: Literal["male", "female", "other", "unknown"]
    birthDate: Optional[str] = None
    deceasedBoolean: Optional[bool] = None
    deceasedDateTime: Optional[str] = None

    def to_json(self) -> dict[str, Any]:
        out = {
            "resourceType": "Patient",
            "id": self.id,
            "active": True,
            "gender": self.gender,
        }
        if self.birthDate:
            out["birthDate"] = self.birthDate
        if self.deceasedBoolean is not None:
            out["deceasedBoolean"] = castBoolean(self.deceasedBoolean)
        if self.deceasedDateTime:
            out["deceasedDateTime"] = self.deceasedDateTime
        return out


@dataclass
class Condition:
    subject: str
    is_present: bool
    snomed_code: int
    text: str

    def to_json(self) -> dict[str, Any]:
        return {
            "resourceType": "Condition",
            "id": str(uuid.uuid4()),
            "clinicalStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-clinical",
                        "code": "active" if self.is_present else "inactive",
                    }
                ]
            },
            "verificationStatus": {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/condition-ver-status",
                        "code": "confirmed" if self.is_present else "refuted",
                    }
                ]
            },
            "code": {
                "coding": [
                    {
                        "system": "http://snomed.info/sct",
                        "code": str(self.snomed_code),
                    }
                ],
                "text": self.text,
            },
            "subject": {"reference": f"Patient/{self.subject}"},
        }


@dataclass
class Observation:
    category: Literal[
        "social-history",
        "vital-signs",
        "imaging",
        "laboratory",
        "procedure",
        "survey",
        "exam",
        "therapy",
        "activity",
    ]
    snomed_code: Optional[str] = None
    loinc_code: Optional[str] = None
    is_true: Optional[bool] = None
    value_quantity: Optional[float] = None
    value_concept: Optional[str] = None

    def to_json(self) -> dict[str, Any]:
        raise NotImplementedError


SUBJECT_SNOMED = [
    ("has_chronic_hematologic_disease", 414022008),
    ("has_asplenia", 707147002),
    ("has_tuberculosis", 427099000),
    ("has_dementia", 52448006),
    ("has_obesity", 414916001),
    ("has_rheumatologic_disorder", 363059001),
    ("has_hiv", 86406008),
    ("has_hypertension", 38341003),
    ("has_malignant_neoplasm", 363346000),
    ("has_malnutrition", 2492009),
    ("has_asthma", 195967001),
    ("has_chronic_cardiac_disease", 128238001),
    ("has_chronic_kidney_disease", 709044004),
    ("has_diabetes", 73211009),
    ("diabetes_type", {"type-1": 46635009, "type-2": 44054006}),
    ("has_liver_disease", 328383001),
    ("has_apnoea", 1023001),
    ("has_inflammatory_bowel_disease", 24526004),
    ("has_rare_disease_inborn_metabolism_error", 86095007),
    ("has_solid_organ_transplant", 161663000),
    ("has_tuberculosis_past", 161414005),
    ("has_immunosuppression", 234532001),
]

SUBJECT_INDICATOR_SNOMED_CODES = dict(SUBJECT_SNOMED)
SNOMED_DISPLAY = dict(
    (v, " ".join(k.split("_")[1:]).capitalize())
    for k, v in SUBJECT_SNOMED
    if isinstance(v, int)
)


def getBirthDate(year: int, month: Optional[int] = None, day: Optional[int] = None):
    s = str(year)
    if month:
        month = int(month)
        s += f"-{month:02d}"
    if day:
        day = int(day)
        s += f"-{day:02d}"
    return s


def castBoolean(s: str) -> Optional[bool]:
    if s.lower() == "true":
        return True
    if s.lower() == "false":
        return False


def subject_to_fhir(row: dict[str, Any]) -> list[dict[str, Any]]:
    out = []
    sex = row.get("sex")
    sex_at_birth = row.get("sex_at_birth")
    # FHIR refers to this as gender, gender identity is elsewhere
    gender = sex or sex_at_birth
    if gender not in ["male", "female"]:
        gender = "unknown" if gender is None else "other"
    out.append(
        Patient(
            row["subject_id"],
            gender,
            getBirthDate(row.get("dob_year"), row.get("dob_month"), row.get("dob_day")),
            deceasedBoolean=row.get("has_died"),
            deceasedDateTime=row.get("date_death"),
        ).to_json()
    )
    for cond in set(row.keys()) & set(SUBJECT_INDICATOR_SNOMED_CODES.keys()):
        if cond == "diabetes_type":
            if row[cond] in SUBJECT_INDICATOR_SNOMED_CODES["diabetes_type"]:
                out.append(
                    Condition(
                        row["subject_id"],
                        is_present=True,
                        snomed_code=SUBJECT_INDICATOR_SNOMED_CODES["diabetes_type"][
                            row[cond]
                        ],
                        text=f"Diabetes: {row[cond]}",
                    ).to_json()
                )
                continue
        if row[cond] in ["True", "False"]:
            out.append(
                Condition(
                    row["subject_id"],
                    is_present=castBoolean(row[cond]),
                    snomed_code=SUBJECT_INDICATOR_SNOMED_CODES[cond],
                    text=SNOMED_DISPLAY[SUBJECT_INDICATOR_SNOMED_CODES[cond]],
                ).to_json()
            )

    return out


def main(file: str):
    with open(file) as fp:
        reader = csv.DictReader(fp)
        for row in reader:
            for output in subject_to_fhir(row):
                print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main(sys.argv[1])
