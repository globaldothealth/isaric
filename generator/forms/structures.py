"""
Contains dictionary structures for standard formats

Dictionary structures which can be called to build up a parser file using a webapp interface.
"""

import streamlit as st
import json
import re


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

    return rule


def field_with_transformation(f: str, d: str, func: str, params: list | None):
    rule = {"field": f, "description": d, "apply": {"function": func}}

    if params:
        rule["apply"]["params"] = params

    return rule


## Combined types


# look for ways to show the 4 options available for this.
def combined_type(rule: str, desc: str, fields: list):
    return {"combinedType": rule, "description": desc, "fields": fields}


### ----------------------------
# Streamlit functions
### ----------------------------


@st.cache_data
def string_to_dict(input_string, conditional=False):
    """
    Transforms a comma-seperated string input (e.g. "1=true, 2=false, 3=false")
    into a dictionary with key:value pairs, converts values into appropriate Python types.
    The conditional flag indicates that there may be a conditional rule which needs parsing
    in addition.
    """

    def convert_vals_recursive(res):
        for k, v in res.items():
            try:
                v_converted = json.loads(v)
            except TypeError:  # dict
                v_converted = convert_vals_recursive(v)
            except:
                v_converted = v
            res[k] = v_converted
        return res

    if input_string == "":
        return {}

    if conditional == True:
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
