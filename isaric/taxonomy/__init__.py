from enum import Enum
from pathlib import Path

from .opencodelists import OpenCodeListsEnum

Sex = Enum("Sex", ["male", "female", "non_binary"])

Pathogen = Enum("Pathogen", ["COVID_19", "MPXV"])

Ethnicity = OpenCodeListsEnum("opensafely/ethnicity-snomed", "2020-04-27")

ReferenceDateType = Enum(
    "ReferenceDateType", ["any_test_confirmation", "laboratory_confirmation"]
)

VisitDuration = Enum(
    "VisitDuration", ["before_admission", "admission", "post_admission"]
)

Outcome = Enum("Outcome", ["death", "recovered"])

Observation = Enum(
    "Observation", (Path(__file__).parent / "observations.txt").read_text()
)
