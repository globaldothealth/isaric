"""
Tests for generator/structures.py
"""

import pytest

# from .forms.structures import search_for_pair
import forms.structures as structures

OBSERVATIONS_INPUT = [
    {
        "name": "bleeding_haemorrhage",
        "date": {"ref": "admissionDateHierachy"},
        "phase": "admission",
        "is_present": {"field": "bleed_ceoccur_v2", "ref": "Y/N/NK"},
        "if": {"bleed_ceoccur_v2": {"!=": 3}},
    },
    {
        "name": "bleeding_haemorrhage",
        "date": {"ref": "admissionDateHierarchy"},
        "phase": "admission",
        "is_present": {"field": "bleed_cetermy_v2", "ref": "Y/N/NK"},
        "if": {"bleed_cetermy_v2 ": {"!=": 3}},
    },
]

COPY_OBSERVATION_INPUT = {
    "name": "bleeding_haemorrhage",
    "date": {"ref": "admissionDateHierachy"},
    "phase": "admission",
    "is_present": {"field": "bleed_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"bleed_ceoccur_v2": {"!=": 3}},
}

REPLACEMENT_OBSERVATION_INPUT = {
    "name": "bleeding_haemorrhage",
    "date": {"ref": "admissionDateHierachy"},
    "phase": "admission",
    "text": {"field": "bleed_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"bleed_ceoccur_v2": {"!=": 3}},
}

NEW_OBSERVATION_INPUT = {
    "name": "bleeding_haemorrhage",
    "date": {"ref": "admissionDateHierachy"},
    "phase": "admission",
    "value": {"field": "bleeding_date", "ref": "Y/N/NK"},
    "if": {"bleeding_date": {"!=": 3}},
}

REPLACED_OBSERVATIONS_OUTPUT = [
    {
        "name": "bleeding_haemorrhage",
        "date": {"ref": "admissionDateHierachy"},
        "phase": "admission",
        "text": {"field": "bleed_ceoccur_v2", "ref": "Y/N/NK"},
        "if": {"bleed_ceoccur_v2": {"!=": 3}},
    },
    {
        "name": "bleeding_haemorrhage",
        "date": {"ref": "admissionDateHierarchy"},
        "phase": "admission",
        "is_present": {"field": "bleed_cetermy_v2", "ref": "Y/N/NK"},
        "if": {"bleed_cetermy_v2 ": {"!=": 3}},
    },
]

ADDED_OBSERVATIONS_OUTPUT = [
    {
        "name": "bleeding_haemorrhage",
        "date": {"ref": "admissionDateHierachy"},
        "phase": "admission",
        "is_present": {"field": "bleed_ceoccur_v2", "ref": "Y/N/NK"},
        "if": {"bleed_ceoccur_v2": {"!=": 3}},
    },
    {
        "name": "bleeding_haemorrhage",
        "date": {"ref": "admissionDateHierarchy"},
        "phase": "admission",
        "is_present": {"field": "bleed_cetermy_v2", "ref": "Y/N/NK"},
        "if": {"bleed_cetermy_v2 ": {"!=": 3}},
    },
    {
        "name": "cough",
        "date": {"ref": "admissionDateHierarchy"},
        "phase": "admission",
        "is_present": {"field": "cough_ceoccur_v2", "ref": "Y/N/NK"},
        "if": {"cough_ceoccur_v2": {"!=": 3}},
    },
    {
        "name": "cough",
        "date": {"ref": "admissionDateHierarchy"},
        "phase": "admission",
        "is_present": {
            "field": "cough_ceoccur_v2_2",
            "values": {1: "true", 2: "true", 3: "true", 0: "false"},
        },
        "if": {"cough_ceoccur_v2_2": {"!=": 4}},
    },
    {
        "name": "bleeding_haemorrhage",
        "date": {"ref": "admissionDateHierachy"},
        "phase": "admission",
        "value": {"field": "bleeding_date", "ref": "Y/N/NK"},
        "if": {"bleeding_date": {"!=": 3}},
    },
]


@pytest.mark.parametrize(
    "dicts,expected",
    [
        ((COPY_OBSERVATION_INPUT, REPLACEMENT_OBSERVATION_INPUT, "field"), True),
        ((COPY_OBSERVATION_INPUT, NEW_OBSERVATION_INPUT, "field"), False),
    ],
)
def test_search_for_pair(dicts, expected):
    dict1, dict2, key = dicts
    assert structures.search_for_pair(dict1, dict2, key) == expected


def test_recursive_search():
    assert (
        structures.recursive_search(COPY_OBSERVATION_INPUT, "field")
        == "bleed_ceoccur_v2"
    )
