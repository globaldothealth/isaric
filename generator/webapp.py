"""
To use, pip install streamlit then run `streamlit run generator/webapp.py` in the terminal.
A locally-hosted website will open in a browser where you can interact with it.
"""

import streamlit as st
import tomli
import tomli_w
import json
import structures
import webapp_attributes

study = {}
subject = {}
visit = {}
observation = {}

# TODO: set to only run when 'generate parser' is clicked.


def string_to_dict(input):
    """
    Transforms a comma-seperated string input (e.g. "1=true, 2=false, 3=false")
    into a dictionary with key:value pairs, converts values into appropriate Python types.
    """
    result = dict(item.split("=") for item in input.split(", "))
    for k, v in result.items():
        try:
            v_converted = json.loads(v)
        except:
            v_converted = v
        result[k] = v_converted

    return result


def field_types(table, attribute, columns):
    col0, col1, col2, col3 = columns

    input_type = col1.selectbox(
        "Type of input field",
        [
            "single field",
            "field with value mapping",
            "field with conditional",
            "date field",
            "field with units",
            "applying a data transformation",
        ],
        key=table + attribute + "type",
    )

    field = col2.text_input("Field (column) name", key=table + attribute + "field")
    desc = col2.text_input("Description", key=table + attribute + "desc")

    if input_type == "single field":
        toml_dict[table][attribute] = structures.single_field(field, desc)

    elif input_type == "field with value mapping":
        col3.write(
            "Value maps can be given either as e.g., '1=alive, 2=hospitalised, 3=death, ...'"
        )
        col3.write(
            "or as a reference to a predefined mapping given in the top section, e.g., 'Y/N/NK'."
        )
        values = col3.text_input(
            "Value mapping given as, e.g., 1=alive, 2=hospitalised, 3=death",
            key=table + attribute + "valuemap",
        )
        try:
            values_transformed = string_to_dict(values)
            toml_dict[table][attribute] = structures.field_value_mapped(
                field, desc, values_transformed
            )
        except:
            toml_dict[table][attribute] = structures.field_value_mapped(
                field, desc, values
            )

    elif input_type == "field with conditional":
        condition = col3.selectbox(
            "The condition to be applied",
            ["if, if.all, if.any"],
            key=table + attribute + "if",
        )
        if condition == "if":
            c_field = col3.text_input(
                "The field to be conditioned on",
                key=table + attribute + "conditionalfield",
            )
            c_value = col3.text_input(
                "The conditional rule",
                value="= 1",
                key=table + attribute + "conditionalvalue",
            )

            toml_dict[table][attribute] = structures.conditional_field(
                field, desc, condition, c_field, c_value
            )

    elif input_type == "date field":
        source_date = col3.text_input(
            "Source date format", value="%d/%m/%Y", key=table + attribute + "sourcedate"
        )
        toml_dict[table][attribute] = structures.field_with_date(
            field, desc, source_date
        )

    elif input_type == "field with units":
        unit = col3.text_input(
            "Desired output unit", value="kg", key=table + attribute + "unit"
        )
        source_unit = col3.text_input(
            "Field name for source unit", key=table + attribute + "sourceunit"
        )
        source_values = col3.text_input(
            "Value mapping for units",
            value="1=kg, 2=lb",
            key=table + attribute + "sourcevalue",
        )
        values = string_to_dict(source_values)

        toml_dict[table][attribute] = structures.field_with_unit(
            field, desc, unit, source_unit, values
        )

    elif input_type == "applying a data transformation":
        apply = col3.selectbox(
            "The transformation to be applied",
            ["isNotNull", "yearsElapsed"],
            key=table + attribute + "apply",
        )
        params = col3.text_input(
            "Parameter fields required by the transformation (optional)",
            key=table + attribute + "applyparam",
        )

        if params == "":
            params = None

        toml_dict[table][attribute] = structures.field_with_transformation(
            field, desc, apply, params
        )


def create_field(table, attribute):
    col0, col1, col2, col3 = st.columns(4)
    if col1.checkbox("Multiple fields to combine?", key=table + attribute + "combine"):
        # need to do an 'add more of these' loop
        columns = col0, col1, col2, col3
        field_types(table, attribute, columns)

    else:
        columns = col0, col1, col2, col3
        field_types(table, attribute, columns)


st.set_page_config(layout="wide")

st.title("Global.health clinical data parser generation")

st.text(
    "This webapp provides semi-automated parser generation for new clinical datasets."
)

st.write(
    "Please fill in the form below to auto-generate a .toml parser file. This will need checking manually before being integrated into the ISARIC repository."
)

with open("generator/base-parser.toml", "rb") as f:
    toml_dict = tomli.load(f)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Study information")
        parser_name = st.text_input("Parser name:", value="isaric-ccpuk")
        parser_descrip = st.text_input("Parser description", value="ISARIC CCPUK study")
        parser_country = st.text_input("Country code:", value="GBR")
        study_date = st.text_input("Study date:", value="2021-01-01")
        pathogen = st.text_input("Pathogen under study:", value="COVID-19")

    toml_dict["adtl"]["name"] = parser_name
    toml_dict["adtl"]["description"] = parser_descrip

    toml_dict["study"]["id"] = parser_name
    toml_dict["study"]["date"] = study_date
    toml_dict["study"]["country_iso3"] = parser_country

    toml_dict["subject"]["study_id"] = parser_name
    toml_dict["subject"]["country_iso3"] = parser_country
    toml_dict["subject"]["pathogen"] = pathogen

    with col2:
        st.header("Common mapping types")
        st.write(
            "Use this section to describe common field mappings - e.g., how the form handles yes/no/not known responses."
        )

        # TODO: need to be able to loop through and add more of these
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            ref = st.text_input("Mapping reference", value="Y/N/NK")

        with subcol2:
            map_key = st.text_input("value pairs", value="1=true, 2=false, 3=false")

        toml_dict["adtl"]["defs"][ref] = structures.predefined_value_maps(
            string_to_dict(map_key)
        )

with open(f"generator/{parser_name}.toml", "wb") as f:
    tomli_w.dump(toml_dict, f)

st.markdown(
    """<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """,
    unsafe_allow_html=True,
)

with st.expander("subjects table"):
    st.header("Subject table")
    st.write(
        "All the available mapping fields (based on the ISARIC schema) for the subject field are listed below."
    )
    st.write(
        "If a given field has a corresponding column in your form, check the box next to it and the section will expand to be filled."
    )
    with open(f"generator/{parser_name}.toml", "rb") as f:
        toml_dict = tomli.load(f)

    for attribute in webapp_attributes.subject_attributes:
        # TODO: This can be packaged up as a function to be called in subject (both cols) and visit (both cols)
        if st.checkbox(attribute, key="subject" + attribute + "selectbox"):
            create_field("subject", attribute)
        st.markdown(
            """<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """,
            unsafe_allow_html=True,
        )

with st.expander("visit table"):
    st.header("Visit table")
    st.write(
        "All the available mapping fields (based on the ISARIC schema) for the visit field are listed below."
    )
    st.write(
        "If a given field has a corresponding column in your form, check the box next to it and the section will expand to be filled."
    )

    for attribute in webapp_attributes.visit_attributes:
        # TODO: This can be packaged up as a function to be called in subject (both cols) and visit (both cols)
        if st.checkbox(attribute, key="visit" + attribute + "selectbox"):
            create_field("visit", attribute)
        st.markdown(
            """<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """,
            unsafe_allow_html=True,
        )

with open(f"generator/{parser_name}.toml", "wb") as f:
    tomli_w.dump(toml_dict, f)
