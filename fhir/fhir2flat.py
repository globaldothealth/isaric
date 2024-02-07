"""
Convert FHIR resources as JSON files to FHIRflat CSV files.
"""

import pandas as pd
import json


def expandCoding(df: pd.DataFrame, column_name: str):
    """
    Expands a column containing a list of dictionaries with coding information into
    multiple columns.
    """

    i = df.columns.get_loc(column_name)
    df.insert(i + 1, column_name + "_system", df[column_name][0][0]["system"])
    df.insert(i + 2, column_name + "_code", df[column_name][0][0]["code"])
    df.insert(i + 3, column_name + "_display", df[column_name][0][0]["display"])

    df.drop(columns=[column_name], inplace=True)


def condenseReference(df, reference):
    """
    Condenses a reference into a string containing the reference type and the reference
    id.
    """
    df[reference] = df[reference].apply(lambda x: x.split("/")[-1])


def fhir2flat(fhir_file: str, flat_file: str):
    """
    Converts a FHIR JSON file into a FHIRflat file.

    fhir_file: path to FHIR JSON file
    flat_file: path to save new FHIRflat CSV file to
    """

    # Load JSON data
    with open(fhir_file) as json_file:
        data = json.load(json_file)

    # Flatten JSON and convert to DataFrame
    df = pd.json_normalize(data)

    # expand all instances of the "coding" list
    for coding in df.columns[df.columns.str.endswith("coding")]:
        expandCoding(df, coding)

    # condense all references
    for reference in df.columns[df.columns.str.endswith("reference")]:
        condenseReference(df, reference)

    # drop static columns
    # Can we drop status in all cases? "status" in MedicationAdministration might be
    # for indicating "not taken"...
    df.drop(columns=["status", "meta.profile"], axis=1, inplace=True)

    # save to csv
    df.to_csv(flat_file, index=False)


fhir2flat("resource_structure_dev/procedure.json", "flat_procedure.csv")
