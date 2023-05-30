"""
Tests for autoparser-toml (make_toml.py)
"""

import pytest
import pandas as pd
from pathlib import Path

import autoparser.make_toml as make_toml
import autoparser.toml_writer as toml_writer

CONFIG = {
    "schema-path": "..",
    "schemas": {
        "subject": "schemas/dev/subject.schema.json",
        "visit": "schemas/dev/visit.schema.json",
        "observation": "schemas/dev/observation.schema.json",
    },
    "categorical_types": ["boolean", "enum", "radio", "dropdown"],
    "text_types": ["text"],
    "choice_delimiter": "|",
    "choice_delimiter_map": ",",
    "lang": {
        "is_missing": [
            "unknown",
            "n/a",
            "n/k",
            "na",
            "nk",
            "not applicable",
            "prefer not to say",
            "not specified",
            "not answered",
        ],
        "is_true": ["y", "yes", "t", "true"],
        "is_false": ["f", "false", "no", "n"],
    },
    "observation_type_mapping": {
        "categorical": "text",
        "boolean": "is_present",
        "yesno": "is_present",
        "radio": "is_present",
        "decimal": "value",
        "integer": "value",
    },
}


@pytest.mark.parametrize(
    "source,expected",
    [
        ("1, yes | 2, no | 3, unknown", ({"1": True, "2": False}, ["3"])),
        ("1, yes | 0, no | 3, unknown", ({"1": True, "0": False}, ["3"])),
        ("yes | no | unknown", (None, [])),
        (
            "kg, weight in kilograms | lbs, weight in pounds",
            ({"kg": "weight in kilograms", "lbs": "weight in pounds"}, []),
        ),
    ],
)
def test_parse_choices(source, expected):
    assert make_toml.parse_choices(CONFIG, source) == expected


def test_map_enum():
    assert make_toml.map_enum(
        ["followup_signs", "info_at_admission2", "followup_symptoms", "during_study5"],
        ["admission", "study", "followup"],
    ) == {"followup_signs": "followup", "followup_symptoms": "followup"}


@pytest.mark.parametrize(
    "source,expected",
    [
        [
            ("observation", "phase"),
            ("enum", ["pre-admission", "admission", "study", "followup"]),
        ]
    ],
)
def test_get_type_enum(source, expected):
    assert make_toml.get_type_enum(CONFIG, *source) == expected


@pytest.mark.parametrize(
    "mapping,expected",
    [
        (
            dict(
                schema_field="sex_at_birth",
                field="sex",
                table="subject",
                category="demographics",
                description="Sex at birth",
                type="radio",
                choices="1, Male | 2, Female | 3, Non-binary | 4, Prefer not to say",
            ),
            dict(
                field="sex",
                description="Sex at birth",
                values={"1": "male", "2": "female", "3": "non_binary"},
            ),
        ),
        (
            dict(
                schema_field="age",
                field="age_estimateyears",
                table="subject",
                category="demographics",
                description="Age/Estimated age",
                type="text",
                choices=None,
            ),
            dict(
                field="age_estimateyears",
                description="Age/Estimated age",
            ),
        ),
    ],
)
def test_single_field_mapping(mapping, expected):
    assert make_toml.single_field_mapping(CONFIG, pd.Series(mapping), {}) == expected


def test_single_field_mapping_with_refs():
    references = {'{"1": true, "2": false}': "Y/N/NK"}
    match = dict(
        schema_field="has_chronic_kidney_disease",
        table="subject",
        field="renal_mhyn",
        type="radio",
        category="comorbidities",
        description="Chronic kidney disease",
        choices="1, YES | 2, NO | 3, Unknown",
        is_required=True,
    )
    assert make_toml.single_field_mapping(CONFIG, pd.Series(match), references) == dict(
        field="renal_mhyn",
        description="Chronic kidney disease",
        ref="Y/N/NK",
    )


def test_make_toml(snapshot):  # integration test
    mappings = pd.concat(
        (
            pd.read_csv(Path(__file__).with_name(f))
            for f in [
                "isaric-subject.csv",
                "isaric-visit.csv",
                "isaric-observation.csv",
            ]
        ),
        ignore_index=True,
    )
    toml_data = make_toml.make_toml(
        CONFIG, mappings, name="test", description="test mappings"
    )
    assert toml_writer.dumps(toml_data) == snapshot
