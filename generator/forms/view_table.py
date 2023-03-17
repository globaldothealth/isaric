"""
Format the dictionary structure as a readable table format (which can eventually be made editable.)
For the subject and visit tables.
"""

import pandas as pd


def view_parser(dict_structure, constants, reverse_order=False):
    dict_structure = dict_structure.copy()
    if reverse_order == True:
        dict_structure = dict(reversed(list(dict_structure.items())))

    if any(x in dict_structure.keys() for x in constants):
        for c in constants:
            dict_structure.pop(c)

    df = pd.DataFrame.from_dict(dict_structure).T
    df = df.reindex(
        columns=[
            "description",
            "combinedType",
            "fields",
            "field",
            "values",
            "unit",
            "source_unit",
            "if",
            "apply",
        ]
    )
    df.reset_index(inplace=True)
    df.rename(columns={"index": "attribute"}, inplace=True)
    if "fields" in df.columns:
        df = df.explode("fields", ignore_index=True)
        # At this point the df has multiple rows for every 'combinedtype', with the 'fields' column containing the whole field/unit/values content.

        # df_fields is the expanded-out version of the 'fields' columns
        idx = df[df.duplicated("attribute", keep=False)]["fields"].index

        df_fields = pd.DataFrame(
            df[df.duplicated("attribute", keep=False)]["fields"].tolist(), index=idx
        )

        c = df.columns.append(df_fields.columns).unique()
        i = df.index.append(df_fields.index).unique()

        df_final = df_fields.combine_first(df).reindex(index=i, columns=c)
        df_final = df_final.drop(["fields"], axis=1)
        return df_final
    else:
        return df
