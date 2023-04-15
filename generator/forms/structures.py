"""
Contains dictionary structures for standard formats

Dictionary structures which can be called to build up a parser file using
a webapp interface.
"""

import streamlit as st
import json
import re


def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")


def predefined_value_maps(values: dict):
    return {"values": values}


def single_field(f, d):
    return {"field": f, "description": d}


def conditional_field(f, d, condition, if_rule, values=None):
    if d == "":
        rule = {"field": f, condition: {}}
    else:
        rule = {"field": f, "description": d, condition: {}}

    if condition != "if":
        log_op = condition.split(".")[1]
        rule.pop(condition)
        rule["if"] = {log_op: []}

    if values:
        value_rule = rule | field_value_mapped(f, d, value_maps=values)
        rule = value_rule

    if isinstance(if_rule, list):
        rule["if"][log_op] = if_rule
    else:
        rule[condition].update(if_rule)

    return rule


def field_with_unit(
    f: str, d: str, unit_f: str, source_unit_f: str, source_unit_v: dict
):
    if d != "":
        return {
            "field": f,
            "description": d,
            "unit": unit_f,
            "source_unit": {"field": source_unit_f, "values": source_unit_v},
        }
    else:
        return {
            "field": f,
            "unit": unit_f,
            "source_unit": {"field": source_unit_f, "values": source_unit_v},
        }


def field_with_date(f: str, d: str, source_date_f: str):
    return {
        "field": f,
        "description": d,
        "date": "%d/%m/%Y",
        "source_date": source_date_f,
    }


def field_value_mapped(f: str, d: str, value_maps: dict | str):
    if isinstance(value_maps, dict):
        rule = {"field": f, "description": d, "values": value_maps}
    else:
        rule = {"field": f, "description": d, "ref": value_maps}

    if rule["description"] == "":
        del rule["description"]

    # if "values" in rule and (rule["values"] == "" or not rule["values"]):
    #     del rule["values"]

    return rule


def field_with_transformation(f: str, d: str, func: str, params: list | None):
    rule = {"field": f, "description": d, "apply": {"function": func}}

    if params:
        rule["apply"]["params"] = params

    return rule


# Combined types


# look for ways to show the 4 options available for this.
def combined_type(rule: str, desc: str, fields: list):
    if desc != "" and desc is not None:
        return {"combinedType": rule, "description": desc, "fields": fields}
    else:
        return {"combinedType": rule, "fields": fields}


def sidebar_search(table):
    """
    Allows user to view, edit, add and delete pre-defined value mappings
    such as 'y/n/nk', some of which may already have been written by autoparser.
    Runs in the app sidebar
    """

    if f"definition_edits_{table}" not in st.session_state:
        st.session_state[f"definition_edits_{table}"] = False

    st.header("Search for pre-defined mappings:")
    ref = st.selectbox(
        "Reference name",
        ["<select>"] + list(st.session_state.toml_dict["adtl"]["defs"].keys()),
        key=f"ref_selectbox_{table}",
        index=0,
    )

    if ref != "<select>":
        if "values" in st.session_state.toml_dict["adtl"]["defs"][ref]:
            st.json(st.session_state.toml_dict["adtl"]["defs"][ref]["values"])
        elif "combinedType" in st.session_state.toml_dict["adtl"]["defs"][ref]:
            st.json(st.session_state.toml_dict["adtl"]["defs"][ref])

        if st.button("Edit/add/delete predefined mappings", key="make-edits"):
            st.session_state[f"definition_edits_{table}"] = True
    else:
        st.session_state[f"definition_edits_{table}"] = False

    if st.session_state[f"definition_edits_{table}"]:
        st.warning(
            "Changes made here will not propegate; any edits or deletions\
                will have to be made manually to any attibutes using them."
        )
        edits = st.radio(
            "Make edits:",
            ["edit this reference", "delete reference", "add new reference"],
            index=0,
        )
        if edits == "edit this reference":
            with st.form("edit", clear_on_submit=True):
                reference = st.text_input("Reference", value=ref)

                if "combinedType" in st.session_state.toml_dict["adtl"]["defs"][ref]:
                    combination_type = st.selectbox(
                        "Which combined type?",
                        ["any", "all", "firstNonNull", "list", "set"],
                        key="MappingscombinationType",
                    )
                    no_fields = st.number_input(
                        "How many fields are there to combine?",
                        value=len(
                            st.session_state.toml_dict["adtl"]["defs"][ref]["fields"]
                        ),
                    )

                    st.write("Fields to combine:")
                    fields = value_map_multi(
                        no_fields,
                        data=st.session_state.toml_dict["adtl"]["defs"][ref]["fields"],
                    )
                else:
                    definition = st.text_input(
                        "Value map",
                        value=", ".join(
                            [
                                f"{k}={v}"
                                for k, v in st.session_state.toml_dict["adtl"]["defs"][
                                    ref
                                ]["values"].items()
                            ]
                        ),
                    )

                add_ref = st.form_submit_button("Edit definition")
                if add_ref:
                    st.session_state.toml_dict["adtl"]["defs"][
                        reference
                    ] = st.session_state.toml_dict["adtl"]["defs"].pop(ref)
                    if (
                        "combinedType"
                        in st.session_state.toml_dict["adtl"]["defs"][ref]
                    ):
                        # fields need combining into one
                        st.session_state.toml_dict["adtl"]["defs"][
                            reference
                        ] = combined_type(combination_type, None, fields)
                    else:
                        st.session_state.toml_dict["adtl"]["defs"][reference][
                            "values"
                        ] = string_to_dict(definition)
                    st.session_state[f"definition_edits_{table}"] = False
                    st.experimental_rerun()

        elif edits == "delete reference":
            delete = st.button("Delete this reference")
            if delete:
                st.session_state.toml_dict["adtl"]["defs"].pop(ref)
                edits = ["edit this reference"]
                delete = False
                st.session_state[f"definition_edits_{table}"] = False
                st.experimental_rerun()

        elif edits == "add new reference":
            combined = st.radio(
                "Multiple fields to combine?", ["No", "Yes"], horizontal=True
            )
            with st.form("add", clear_on_submit=True):
                reference = st.text_input("Reference")
                if combined == "No":
                    definition = st.text_input("Value map")
                else:
                    combination_type = st.selectbox(
                        "Which combined type?",
                        ["any", "all", "firstNonNull", "list", "set"],
                        key="MappingscombinationTypeAdd",
                    )
                    no_fields = st.number_input(
                        "How many fields are there to combine?",
                        value=2,
                    )

                    st.write("Fields to combine:")
                    fields = value_map_multi(no_fields)

                add_ref = st.form_submit_button("Add mapping to definitions")
                if add_ref:
                    st.session_state.toml_dict["adtl"]["defs"][reference] = {}
                    if combined:
                        st.session_state.toml_dict["adtl"]["defs"][
                            reference
                        ] = combined_type(combination_type, None, fields)
                    else:
                        st.session_state.toml_dict["adtl"]["defs"][reference][
                            "values"
                        ] = string_to_dict(definition)
                    edits = "edit this reference"
                    st.session_state[f"definition_edits_{table}"] = False
                    st.experimental_rerun()


def value_map_multi(nrows, data=None):
    """
    Provides fields for value maps where multiple fields are combined.
    Returns a list of the fields.
    """

    fields = []

    mf_grid = make_grid(nrows * 2, 2)

    for i, j in zip(range(0, nrows * 2, 2), range(nrows)):
        cell1, cell2 = mf_grid[i][0], mf_grid[i][1]
        with cell1:
            field_name = st.text_input(
                f"Field name ({j})",
                key="keymaps_fields" + str(i),
                value=data[j]["field"] if data else "",
            )
            st.markdown("#")
            st.markdown("###")
            descrip = st.text_input(
                "Description (optional)",
                key="keymaps_description" + str(i),
                value=data[j]["description"]
                if (data and "description" in data[j])
                else "",
            )
        with cell2:
            if "values" in data[j]:
                val_map = st.text_area(
                    "Value map (optional)",
                    value=", ".join([f"{k}={v}" for k, v in data[j]["values"].items()]),
                    key="keymaps_values" + str(i),
                )
            else:
                val_map = st.text_area(
                    "Value map (optional)",
                    key="keymaps_values" + str(i),
                    placeholder="2=slight, 3=moderate, 4=severe, 5=unable",
                )

            if "if" in data[j]:
                conditional = st.text_input(
                    "Condition (optional)",
                    value=", ".join([f"{k}={v}" for k, v in data[j]["if"].items()]),
                    key="keymaps_condition" + str(i),
                )
            else:
                conditional = st.text_input(
                    "Condition (optional)",
                    key="keymaps_condition" + str(i),
                    placeholder="dsterm=4",
                )
        if conditional != "":
            if val_map != "":
                fields.append(
                    conditional_field(
                        field_name,
                        descrip,
                        "if",
                        string_to_dict(conditional, conditional=True),
                        values=string_to_dict(val_map),
                    )
                )
            else:
                fields.append(
                    conditional_field(
                        field_name,
                        descrip,
                        "if",
                        string_to_dict(conditional, conditional=True),
                    )
                )
        elif val_map != "":
            fields.append(
                field_value_mapped(
                    field_name,
                    descrip,
                    values=string_to_dict(val_map),
                )
            )
        else:
            fields.append(single_field(field_name, descrip))

        for square in [
            mf_grid[i + 1][0],
            mf_grid[i + 1][1],
        ]:
            square.markdown("#")
            square.markdown("#")

    return fields


# ---------------------------------------------------------
# Streamlit functions
# ---------------------------------------------------------


@st.cache_data
def string_to_dict(input_string, conditional=False):
    """
    Transforms a comma-seperated string input (e.g. "1=true, 2=false, 3=false")
    into a dictionary with key:value pairs, converts values into appropriate Python
    types. The conditional flag indicates that there may be a conditional rule which
    needs parsing in addition.
    """

    def convert_vals_recursive(res):
        for k, v in res.items():
            try:
                v_converted = json.loads(v)
            except TypeError:  # dict
                v_converted = convert_vals_recursive(v)
            except json.decoder.JSONDecodeError:
                v_converted = v
            res[k] = v_converted
        return res

    if input_string == "":
        return {}

    if conditional is True:
        result = [re.split("([<>=!]+)", item) for item in input_string.split(", ")]
        for item in result:
            if item[1] == "=":
                del item[1]
            else:
                item[1] = {item[1]: item[2]}
                del item[2]
        result = dict(result)

    else:
        result = dict(item.split("=") for item in input_string.split(", "))

    return convert_vals_recursive(result)


def make_grid(cols, rows):
    # creates a grid layout in streamlit
    grid = [0] * cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid


def recursive_search(dict_2_search, key):
    """
    Search for a specific key in a nested dictionary.
    Can't account for other data structures, lists etc.
    """

    if key in dict_2_search:
        return dict_2_search[key]
    for v in dict_2_search.values():
        if isinstance(v, dict):
            returned_field = recursive_search(v, key)
            if returned_field is not None:
                return returned_field


def search_for_pair(old_observation, new_observation, key):
    """
    Returns True if both dicts contain a key with the same value regardless
     of that key's location.
    """

    field1 = recursive_search(old_observation, key)
    field2 = recursive_search(new_observation, key)

    if field1 == field2:
        return True
    else:
        return False
