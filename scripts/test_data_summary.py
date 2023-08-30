"""
Tests data summary
```
"""
from data_summary import main

TEST_DATA = "test_data.csv"


def test_data_summary():
    assert main(
        TEST_DATA, parser_name="isaric/parsers/parser.toml", id_field="record_id"
    ) == dict(
        encoding="utf-8-sig",
        file="test_data.csv",
        id_field="record_id",
        parser="isaric/parsers/parser.toml",
        mimetype="text/csv",
        n_id=2,
        non_empty_fields=["diabetes_mhyn", "record_id", "renal_mhyn"],
        sha256="54662f93278668a7591cfb7a9c3cfb237100893b7b92a91331dddf9e1ce8ab6d",
    )
