"""
Tests for REDCap RELSUB matcher
"""

import pytest
import relsub

DATA = [
    {"left": "a", "right": "b"},
    {"left": "b", "right": "c"},
    {"left": "c", "right": "d"},
    {"left": "e", "right": "f"},
    {"left": "f", "right": "e"},
    {"left": "g", "right": "h"},
]

DATA_DELIMITED = [
    {"left": "a", "right": "b ; c ; d"},
    {"left": "e", "right": "f"},
    {"left": "g", "right": "h"},
]

MATCHED = {
    "a": 1,
    "b": 1,
    "c": 1,
    "d": 1,
    "e": 2,
    "f": 2,
    "g": 3,
    "h": 3,
}


@pytest.mark.parametrize(
    "source,expected", [(DATA, MATCHED), (DATA_DELIMITED, MATCHED)]
)
def test_relsub_matcher(source, expected):
    assert relsub.relsub_matcher(source, "left", "right") == expected
