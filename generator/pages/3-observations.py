# observations.py

import streamlit as st
import tomli
import tomli_w
import json
import structures
import re
import pandas as pd

from webapp import generate_parser, string_to_dict

if "obs_list" not in st.session_state:
    st.session_state.obs_list = []

df = pd.DataFrame(st.session_state.obs_list)

st.header("Observations table")
st.write(
    "All the available mapping fields (based on the ISARIC schema) for the observations table are listed below. \
        Constant fields will be taken automatically from the study-level table on the home page."
)
st.write(
    "For every observation in your form, fill in this form. When the 'add this observation to the data store' button is clicked, it will be added to memory.\
        The currently stored observations are listed under the form. Observations which are already present can be overwritten\
             by filling in the form with the same observation name and phase."
)

st.markdown("#")

with st.form(key="observation", clear_on_submit=True):
    st.write("Required fields:")
    (
        col1,
        col2,
    ) = st.columns(2)
    with col1:
        name = st.selectbox(
            "Observation name", st.session_state.obs["properties"]["name"]["enum"]
        )
        phase = st.radio(
            "Observation phase", ["admission", "study", "followup"], horizontal=True
        )
    with col2:
        date = st.text_input(
            "Date of observation",
            value="admissionDateHierarchy",
            help="This can either be a single field name where the date is stored,\
                              or a reference to a pre-defined date hierarchy.",
        )
        condition = st.text_input(
            "Condition required to show this observation as a row, e.g. 'cmyn=1'"
        )

    st.markdown("#")
    st.write("Optional fields")

    (
        col1,
        col2,
    ) = st.columns(2)

    with col1:
        st.write(
            "**is_present**: Records if the observation denotes presence (*true*) or absence (*false*) of the symptom."
        )
        subcol1, subcol2 = st.columns(2)
        is_present_field = subcol1.text_input("Field name", key="ispresent_field")
        is_present_values = subcol2.text_input("Value map", key="ispresent_value")
        st.write("Values: Records the value of **numerical observations**")
        value_field = st.text_input(
            "Field name",
            help="For numerical values - E.g., 'diabp_vsorres' storing the recorded blood pressure for the observation.",
            key="value_field",
        )
        subcol1, subcol2, subcol3 = st.columns(3)
        value_units = subcol1.text_input(
            "Desired unit for value (optional)",
            placeholder="kg",
            help="Desired unit for the value field, e.g. kg for mass, '°C' for temperature, years for age.",
            key="value_units_required",
        )
        value_sunit_field = subcol2.text_input(
            "Unit source field (optional)",
            help="Field name where the unit of the measurement taken is recorded",
            key="value_units_source",
        )
        value_sunits_map = subcol3.text_input(
            "Unit field mapping (optional)",
            placeholder="1=kg, 2=lbs",
            help="",
            key="value_units_map",
        )
        st.write("Text: records value map for **text-based observations**")
        subcol1, subcol2 = st.columns(2)
        text_field = subcol1.text_input("Field name", key="text_field")
        text_values = subcol2.text_input(
            "Value map",
            help="For text observations - E.g., for a conciousness scale, field = 'avpu_vsorres', values = '1=Alert, 2=Verbal, 3=Pain, 4=Unresponsive' }.",
            key="text_value",
        )
    with col2:
        st.write(
            "**Occurance period**: ISO 8601 duration string referring to the time period before the date in which observation occurred"
        )
        occurence_period = st.text_input("Field name")
        st.write("**Context**: Context that qualifies the observation")
        context = st.text_input(
            "Field name",
            help="e.g. *axillary* temperature, or *room air* oxygen saturation measurement",
        )

        st.write("")
        st.write("")
        subcol1, subcol2, subcol3 = st.columns([1, 4, 1])
        add_observation = subcol2.form_submit_button(
            label="Add this observation field to data store"
        )

    if add_observation:
        # check for potential dictionary entries
        try:
            is_present_values = string_to_dict(is_present_values)
        except:
            pass

        try:
            text_values = string_to_dict(text_values)
        except:
            pass

        if value_units != "":
            value = structures.field_with_unit(
                value_field, "", value_units, value_sunit_field, value_sunits_map
            )
        else:
            value = value_field

        # write to a data store
        observation = {
            "name": name,
            "date": date,
            "phase": phase,
            "is_present": structures.field_value_mapped(
                is_present_field, "", is_present_values
            ),
            "if": string_to_dict(condition, conditional=True),
            "value": value,
            "text": structures.field_value_mapped(text_field, "", text_values),
            "occurence_period": occurence_period,
            "context": context,
        }

        optional = ["is_present", "value", "text", "occurence_period", "context"]
        for f in optional:
            if observation[f] == "":
                del observation[f]
            elif type(observation[f]) == dict:
                if observation[f]["field"] == "":
                    del observation[f]

        # here, search for whether the key has been written before, and overwrite if it has.
        overwrite = False
        for i, d in enumerate(st.session_state.obs_list):
            if d["name"] == observation["name"] and d["phase"] == observation["phase"]:
                st.session_state.obs_list[i] = observation
                overwrite = True
                break

        if overwrite == False:
            st.session_state.obs_list.append(observation)

        # df = pd.json_normalize(st.session_state.obs_list, max_level=0)
        df = pd.DataFrame(st.session_state.obs_list)


_, col2, col3, _ = st.columns(4)

parser_name = st.session_state.toml_dict["adtl"]["name"]

if col2.button(
    "Generate Parser", type="primary", use_container_width=True, key="parsergen-subject"
):
    if generate_parser(st.session_state.toml_dict):
        col2.write("Parser generated! Available in the 'generator' folder.")
        with open(f"generator/{parser_name}-generator.toml", "rb") as f:
            col3.download_button(
                label="Download Parser",
                data=f,
                file_name=f"{parser_name}.toml",
                use_container_width=True,
            )

st.markdown("### Observations currently stored in memory")
st.table(df)
