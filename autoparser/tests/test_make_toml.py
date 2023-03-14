"""
Tests for autoparser-toml (make_toml.py)
"""

import autoparser.make_toml as make_toml
import pytest

CONFIG = {
    "schema-path": "..",
    "schemas": {
        "subject": "schemas/dev/subject.schema.json",
        "visit": "schemas/dev/visit.schema.json",
        "observation": "schemas/dev/observation.schema.json",
    },
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
}


@pytest.mark.parametrize(
    "source,expected",
    [
        ("1, yes | 2, no | 3, unknown", ({"1": True, "2": False}, ["3"])),
        ("1, yes | 0, no | 3, unknown", ({"1": True, "0": False}, ["3"])),
        (
            "kg, weight in kilograms | lbs, weight in pounds",
            ({"kg": "weight in kilograms", "lbs": "weight in pounds"}, []),
        ),
    ],
)
def test_parse_choices(source, expected):
    assert make_toml.parse_choices(CONFIG, source) == expected


def test_invalid_parse_choices():
    with pytest.raises(ValueError, match="parse_choices"):
        make_toml.parse_choices(CONFIG, "yes | no | unknown")


def test_map_enum():
    assert make_toml.map_enum(
        ["followup_signs", "info_at_admission2", "followup_symptoms", "during_study5"],
        ["admission", "study", "followup"],
    ) == {"followup_signs": "followup", "followup_symptoms": "followup"}


@pytest.mark.parametrize(
    "source,expected",
    [[("observation", "phase"), ("enum", ["admission", "study", "followup"])]],
)
def test_get_type_enum(source, expected):
    assert make_toml.get_type_enum(CONFIG, *source) == expected


def test_single_field_mapping():
    pass


def test_make_toml_table():
    pass


def test_make_toml():
    pass


def test_common_mappings():
    pass
