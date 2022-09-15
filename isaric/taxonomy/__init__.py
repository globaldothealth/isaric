from enum import Enum

from .opencodelists import OpenCodeListsEnum

Sex = Enum("Sex", "male female non_binary")

Pathogen = Enum("Pathogen", "COVID_19 MPXV")

Ethnicity = OpenCodeListsEnum("opensafely/ethnicity-snomed", "2020-04-27")

ReferenceDateType = Enum(
    "ReferenceDateType", "any_test_confirmation laboratory_confirmation"
)

Outcome = Enum("Outcome", "Death Recovered")
