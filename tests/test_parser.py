import pytest

import isaric.parser as parser

RULE_SINGLE_FIELD = {"field": "diabetes_mhyn"}
RULE_SINGLE_FIELD_WITH_MAPPING = {
    "field": "diabetes_mhyn",
    "values": {"1": True, "2": False, "3": None},
}

LIVER_DISEASE = [
    {
        "field": "modliv",
        "values": {"1": True, "0": False, "2": None},
        "description": "Moderate liver disease",
    },
    {
        "field": "mildliver",
        "values": {"1": True, "0": False, "2": None},
        "description": "Mild liver disease",
    },
]


RULE_COMBINED_TYPE_ANY = {"combinedType": "any", "fields": LIVER_DISEASE}
RULE_COMBINED_TYPE_ALL = {"combinedType": "all", "fields": LIVER_DISEASE}
RULE_COMBINED_FIRST_NON_NULL = {
    "combinedType": "firstNonNull",
    "fields": [{"field": "first"}, {"field": "second"}],
}

RULE_NON_SENSITIVE = {"field": "id"}
RULE_SENSITIVE = {"field": "id", "sensitive": True}


@pytest.mark.parametrize(
    "row_rule,expected",
    [
        (({"diabetes_mhyn": "1"}, RULE_SINGLE_FIELD_WITH_MAPPING), True),
        (({"diabetes_mhyn": "1"}, RULE_SINGLE_FIELD), "1"),
        (({}, "CONST"), "CONST"),
        (({"modliv": "1", "mildliver": "0"}, RULE_COMBINED_TYPE_ANY), True),
        (({"modliv": "1", "mildliver": "0"}, RULE_COMBINED_TYPE_ALL), False),
        (({"id": "1"}, RULE_NON_SENSITIVE), "1"),
        (
            ({"id": "1"}, RULE_SENSITIVE),
            "6b86b273ff34fce19d6b804eff5a3f5747ada4eaa22f1d49c01e52ddb7875b4b",
        ),
        (({"first": "1", "second": ""}, RULE_COMBINED_FIRST_NON_NULL), "1"),
        (({"first": "1", "second": "2"}, RULE_COMBINED_FIRST_NON_NULL), "1"),
        (({"first": "2", "second": "1"}, RULE_COMBINED_FIRST_NON_NULL), "2"),
        (({"first": "", "second": "3"}, RULE_COMBINED_FIRST_NON_NULL), "3"),
    ],
)
def test_get_value(row_rule, expected):
    row, rule = row_rule
    assert parser.get_value(row, rule) == expected
