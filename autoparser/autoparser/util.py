"""
Common utility functions for autoparser
"""
import json
import logging
from typing import Any, Dict
from pathlib import Path

import tomli

DEFAULT_CONFIG = "config/redcap-en.toml"


def maybe(x, func, default=None):
    return func(x) if x is not None else default


def read_data(path: Path) -> Dict:
    if path.suffix == ".json":
        with path.open() as fp:
            return json.load(fp)
    elif path.suffix == ".toml":
        with path.open("rb") as fp:
            return tomli.load(fp)


def parse_choices(config: Dict[str, Any], s: str) -> Dict[str, Any]:
    delimiter = config["choice_delimiter"]
    delimiter_map = config["choice_delimiter_map"]
    lang = config["lang"]
    lower_string = lambda s: s.strip().lower()  # NOQA
    if not isinstance(s, str):
        return None, []
    choices_list = [
        tuple(map(lower_string, x.split(delimiter_map)[:2])) for x in s.split(delimiter)
    ]
    if any(len(c) != 2 for c in choices_list):
        logging.info("Invalid choices list {choices_list!r}, returning None")
        return None, []
    try:
        choices = dict(
            tuple(map(lower_string, x.split(delimiter_map)[:2]))
            for x in s.split(delimiter)
        )
    except ValueError:
        logging.warning(
            f"parse_choices({s!r}) failed with delimiter={delimiter!r} delimiter_map={delimiter_map!r}"
        )
        return None, []
    # drop n/a, n/k, unknowns
    nulls = [k for k, v in choices.items() if v in lang["is_missing"]]
    choices = {k: v for k, v in choices.items() if v not in lang["is_missing"]}
    for k, v in choices.items():
        if v in lang["is_true"]:
            choices[k] = True
        if v in lang["is_false"]:
            choices[k] = False
    return choices, nulls
