import json
from enum import Enum
from pathlib import Path
from functools import cache

TAXONOMY_VERSION = "1"


@cache
def load_taxonomy(kind: str, version: str):
    taxonomy_file = Path(__file__).parent / f"v{version}.json"
    with open(taxonomy_file) as fp:
        taxonomy = json.load(fp)
        assert taxonomy["version"] == version
        types = taxonomy["types"]
        if kind in types:
            return Enum(kind, types[kind])


Diabetes = load_taxonomy("Diabetes", TAXONOMY_VERSION)
Ethnicity = load_taxonomy("Ethnicity", TAXONOMY_VERSION)
Observation = load_taxonomy("Observation", TAXONOMY_VERSION)
Outcome = load_taxonomy("Outcome", TAXONOMY_VERSION)
Pathogen = load_taxonomy("Pathogen", TAXONOMY_VERSION)
Phase = load_taxonomy("Pathogen", TAXONOMY_VERSION)
PregnancyGestationalOutcome = load_taxonomy(
    "PregnancyGestationalOutcome", TAXONOMY_VERSION
)
ReferenceDate = load_taxonomy("ReferenceDate", TAXONOMY_VERSION)
Sex = load_taxonomy("Sex", TAXONOMY_VERSION)
Smoker = load_taxonomy("Smoker", TAXONOMY_VERSION)
VisitDuration = load_taxonomy("VisitDuration", TAXONOMY_VERSION)
