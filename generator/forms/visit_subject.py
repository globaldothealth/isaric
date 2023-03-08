import streamlit as st
import forms.structures as structures

from forms.structures import string_to_dict, make_grid


def field_types(table, attribute, a_type, columns, iterable="0"):
    col0, col1, col2, col3 = columns

    if a_type == "boolean" or type(a_type) == list:
        i = 1
        if type(a_type) == list:
            optional_vals = ", ".join([f"{i+1}={v}" for i, v in enumerate(a_type)])
        else:
            optional_vals = "Y/N/NK"
    else:
        i = 0
        optional_vals = None

    input_type = col1.selectbox(
        "Type of input field",
        [
            "single field",
            "field with value mapping",
            "single field with conditional",
            "value mapped with conditional",
            "date field",
            "field with units",
            "applying a data transformation",
        ],
        key=table + attribute + iterable + "type",
        index=i,
    )

    field = col2.text_input(
        "Field (column) name", key=table + attribute + iterable + "field"
    )
    desc = col2.text_input("Description", key=table + attribute + iterable + "desc")

    if input_type == "single field":
        return structures.single_field(field, desc)

    elif input_type == "field with value mapping":
        col3.write(
            "Value maps can be given either as e.g., '1=alive, 2=hospitalised, 3=death, ...'"
        )
        col3.write(
            "or as a reference to a predefined mapping given in the top section, e.g., 'Y/N/NK'."
        )
        values = col3.text_input(
            "Value mapping given as, e.g., 1=alive, 2=hospitalised, 3=death",
            key=table + attribute + iterable + "valuemap",
            value=optional_vals,
        )
        try:
            values_transformed = string_to_dict(values)
            return structures.field_value_mapped(field, desc, values_transformed)
        except:
            return structures.field_value_mapped(field, desc, values)

    elif "with conditional" in input_type:
        if input_type == "value mapped with conditional":
            values = col2.text_input(
                "Value mapping given as, e.g., 1=alive, 2=hospitalised, 3=death, or refer to predefined maps e.g.Y/N/NK",
                key=table + attribute + iterable + "valuemap",
                value=optional_vals,
            )
            try:
                values_transformed = string_to_dict(values)
            except:
                values_transformed = values
        else:
            values_transformed = None

        condition = col3.selectbox(
            "The condition to be applied",
            ["if", "if.all", "if.any"],
            key=table + attribute + iterable + "if",
        )
        if condition == "if":
            c_rule = col3.text_input(
                "The conditional rule, e.g. other_cmyn=1, with no spaces.",
                key=table + attribute + iterable + "conditionalfield",
            )

            if "," in c_rule:
                error = ValueError(
                    "Only one conditional rule can be entered if a combined option is not selected.\n\
                           Please either change the condition being applied to if.all or if.any, or remove the additional conditions."
                )
                st.exception(error)

            return structures.conditional_field(
                field,
                desc,
                condition,
                string_to_dict(c_rule, conditional=True),
                values_transformed,
            )
        elif condition == "if.any" or condition == "if.all":
            c_rule = col3.text_input(
                "List the conditional rules, e.g. other_cmyn=1, daily+cmyn>=2.",
                key=table + attribute + iterable + "conditionalfield",
            )

            c_rule_transformed = [
                {k: v} for k, v in string_to_dict(c_rule, conditional=True).items()
            ]

            return structures.conditional_field(
                field, desc, condition, c_rule_transformed, values_transformed
            )

    elif input_type == "date field":
        source_date = col3.text_input(
            "Source date format",
            value="%d/%m/%Y",
            key=table + attribute + iterable + "sourcedate",
        )
        return structures.field_with_date(field, desc, source_date)

    elif input_type == "field with units":
        unit = col3.text_input(
            "Desired output unit", value="kg", key=table + attribute + iterable + "unit"
        )
        source_unit = col3.text_input(
            "Field name for source unit",
            key=table + attribute + iterable + "sourceunit",
        )
        source_values = col3.text_input(
            "Value mapping for units",
            value="1=kg, 2=lb",
            key=table + attribute + iterable + "sourcevalue",
        )
        values = string_to_dict(source_values)

        return structures.field_with_unit(field, desc, unit, source_unit, values)

    elif input_type == "applying a data transformation":
        apply = col3.selectbox(
            "The transformation to be applied",
            ["isNotNull", "yearsElapsed"],
            key=table + attribute + iterable + "apply",
        )
        params = col3.text_input(
            "Parameter fields required by the transformation (optional)",
            key=table + attribute + iterable + "applyparam",
        )

        if params == "":
            params = None

        return structures.field_with_transformation(field, desc, apply, params)


def create_field(table, attribute, a_type, num_cols: int | list):
    col0, col1, col2, col3 = st.columns(num_cols)
    if col1.checkbox("Multiple fields to combine?", key=table + attribute + "combine"):
        combination_type = col1.selectbox(
            "Which combined type should be applied?",
            ["any", "all", "firstNonNull", "list"],
            key=table + attribute + "combinationType",
        )
        comb_desc = col1.text_input(
            "Description", key=table + attribute + "combinationdesc"
        )
        no_fields = col1.number_input(
            "How many fields are there to combine?",
            value=2,
            key=table + attribute + "multifield",
        )

        fields = []

        mf_grid = make_grid(no_fields * 2, num_cols)

        for i in range(0, no_fields * 2, 2):
            columns = mf_grid[i][0], mf_grid[i][1], mf_grid[i][2], mf_grid[i][3]
            field = field_types(table, attribute, a_type, columns, iterable=str(i))
            fields.append(field)
            for square in [
                mf_grid[i + 1][0],
                mf_grid[i + 1][1],
                mf_grid[i + 1][2],
                mf_grid[i + 1][3],
            ]:
                square.markdown("#")

        return structures.combined_type(combination_type, comb_desc, fields)

    else:
        columns = st.columns(num_cols)
        return field_types(table, attribute, a_type, columns)
