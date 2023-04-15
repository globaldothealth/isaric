"""
Tests for generator/forms
"""

import pytest

import forms.observation as observation

DIRTY_OBSERVATION_BASIC = {
    "name": "abdominal_pain",
    "date": "admissionDateHierarchy",
    "phase": "admission",
    "is_present": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"abdiopain_ceoccur_v2 ": {"!=": 0}},
    "value": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "text": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "start_date": "",
    "duration_type": "event",
    "context": {
        "combinedType": "set",
        "fields": [{"field": "", "values": {}, "description": ""}],
    },
}

DIRTY_OBSERVATION_CONTEXT = {
    "name": "abdominal_pain",
    "date": "admissionDateHierarchy",
    "phase": "admission",
    "is_present": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"abdiopain_ceoccur_v2 ": {"!=": 0}},
    "value": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "text": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "start_date": "",
    "duration_type": "event",
    "context": {
        "combinedType": "set",
        "fields": [
            {
                "field": "oxy_vsorresu",
                "values": {"1": "Room air", "2": "Oxygen therapy"},
            }
        ],
    },
}

CLEAN_OBSERVATION_IS_PRESENT = {
    "name": "abdominal_pain",
    "date": "admissionDateHierarchy",
    "phase": "admission",
    "is_present": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"abdiopain_ceoccur_v2 ": {"!=": 0}},
    "duration_type": "event",
}

CLEAN_OBSERVATION_IS_PRESENT_CONTEXT = {
    "name": "abdominal_pain",
    "date": "admissionDateHierarchy",
    "phase": "admission",
    "is_present": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"abdiopain_ceoccur_v2 ": {"!=": 0}},
    "duration_type": "event",
    "context": {
        "combinedType": "set",
        "fields": [
            {
                "field": "oxy_vsorresu",
                "values": {"1": "Room air", "2": "Oxygen therapy"},
            }
        ],
    },
}

CLEAN_OBSERVATION_TEXT = {
    "name": "abdominal_pain",
    "date": "admissionDateHierarchy",
    "phase": "admission",
    "text": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"abdiopain_ceoccur_v2 ": {"!=": 0}},
    "duration_type": "event",
}

CLEAN_OBSERVATION_VALUE = {
    "name": "abdominal_pain",
    "date": "admissionDateHierarchy",
    "phase": "admission",
    "value": {"field": "abdiopain_ceoccur_v2", "ref": "Y/N/NK"},
    "if": {"abdiopain_ceoccur_v2 ": {"!=": 0}},
    "duration_type": "event",
}


@pytest.mark.parametrize(
    "inputs,expected",
    [
        ((DIRTY_OBSERVATION_BASIC, "presence/absence"), CLEAN_OBSERVATION_IS_PRESENT),
        (
            (DIRTY_OBSERVATION_CONTEXT, "presence/absence"),
            CLEAN_OBSERVATION_IS_PRESENT_CONTEXT,
        ),
        ((DIRTY_OBSERVATION_BASIC, "text"), CLEAN_OBSERVATION_TEXT),
        ((DIRTY_OBSERVATION_BASIC, "value"), CLEAN_OBSERVATION_VALUE),
    ],
)
def test_observations_are_being_cleaned(inputs, expected):
    obs, obstype = inputs
    assert observation.cleanup_observation(obs, obstype) == expected
