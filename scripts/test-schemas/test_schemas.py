"""
Test schemas.
"""
import json
from pathlib import Path

import fastjsonschema
import pytest

SCHEMA_PATH = Path("schemas/dev")


def load_schema(path: str):
    with (SCHEMA_PATH / path).open() as fp:
        return fastjsonschema.compile(json.load(fp))


validate_observation = load_schema("observation.schema.json")

INVALID_OBSERVATIONS = [
    {
        "date": "2022-05-05",
        "name": "respiratory_rate",
        "phase": "study",
        "text": "good",
    },
    {"date": "2022-05-05", "name": "avpu", "phase": "study", "text": "alert"},
    {
        "date": "2022-05-05",
        "name": "inability_to_walk_scale",
        "phase": "study",
        "text": "alert",
    },
    {
        "date": "2022-05-05",
        "name": "inability_to_walk_scale",
        "phase": "study",
        "value": 5,
    },
    {
        "date": "2022-05-05",
        "name": "richmond_agitation-sedation_scale",
        "phase": "study",
        "value": -6,
    },
    {"date": "2022-05-05", "name": "headache", "phase": "study", "value": -6},
    {"date": "2022-05-05", "name": "headache", "phase": "study", "is_present": -6},
]
VALID_OBSERVATIONS = [
    {"date": "2022-05-05", "name": "respiratory_rate", "phase": "study", "value": 20},
    {"date": "2022-05-05", "name": "avpu", "phase": "study", "text": "Alert"},
    {
        "date": "2022-05-05",
        "name": "inability_to_walk_scale",
        "phase": "study",
        "value": 4,
    },
    {
        "date": "2022-05-05",
        "name": "richmond_agitation-sedation_scale",
        "phase": "study",
        "value": 0,
    },
    {"date": "2022-05-05", "name": "headache", "phase": "study", "is_present": True},
    # Additional properties are allowed as long as the required properties are present
    {
        "date": "2022-05-05",
        "name": "headache",
        "phase": "study",
        "is_present": True,
        "text": "Migraine",
    },
]


@pytest.mark.parametrize("value", INVALID_OBSERVATIONS)
def test_invalid_observations(value):
    with pytest.raises(fastjsonschema.JsonSchemaException):
        validate_observation(value)


@pytest.mark.parametrize("value", VALID_OBSERVATIONS)
def test_valid_observations(value):
    validate_observation(value)
