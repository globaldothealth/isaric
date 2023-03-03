# observations.py

import streamlit as st
import tomli
import tomli_w
import json
import structures
import re

from webapp import generate_parser, string_to_dict

if "obs_list" not in st.session_state:
    st.session_state.obs_list = []

st.header("Observations table")
st.write(
    "All the available mapping fields (based on the ISARIC schema) for the observations table are listed below. \
        Constant fields will be taken automatically from the study-level table on the home page."
)
st.write(
    "For every observation in your form, fill in this form. When the 'add this observation to the data store' button is clicked, it will be added to memory.\
        The currently stored observations are listed under the form."
)

st.markdown("#")

obs_id = st.text_input("Observation ID field")
try:
    subject_id = st.session_state.toml_dict["visit"]["subject_id"]["field"]
    visit_id = st.session_state.toml_dict["visit"]["visit_id"]["field"]
except:
    subject_id = st.text_input("Subject ID field (you only need to input this once)")
    # st.session_state.toml_dict["visit"]["subject_id"]["field"] = subject_id

    visit_id = st.text_input("Visit ID field (you only need to input this once)")
    # st.session_state.toml_dict["visit"]["visit_id"]["field"] = visit_id

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
        date = st.text_input("Date of observation", value="admissionDateHierarchy")
        condition = st.text_input("If a condition is relevent, enter it here as cmyn=1")

    st.markdown("#")
    st.write("Optional fields")

    (
        col1,
        col2,
    ) = st.columns(2)

    with col1:
        st.write(
            "Field name and values if the observation denotes presence (*true*) or absence (*false*)"
        )
        subcol1, subcol2 = st.columns(2)
        is_present_field = subcol1.text_input("Field name")
        is_present_values = subcol2.text_input("Value map")
        value = st.text_input(
            "Field name for the value of numerical observations",
            help="For numerical values - E.g., 'diabp_vsorres' storing the recorded blood pressure for the observation.",
        )
        text = st.text_input(
            "Field name for the value of the observation",
            help="For numerical values - E.g., 'diabp_vsorres' storing the recorded blood pressure for the observation.",
        )  # value_char in rapid observations - need field for name and field for mapped values.
    with col2:
        st.write("")
        st.write("")
        occurence_period = st.text_input(
            "ISO 8601 duration string referring to the time period before the date in which observation occurred"
        )
        context = st.text_input(
            "Context that qualifies the observation, e.g. *axillary* temperature, or *room air* oxygen saturation measurement"
        )

        add_observation = st.form_submit_button(
            label="Add this observation field to data store"
        )

    if add_observation:
        # check for potential dictionary entries
        try:
            is_present_values = string_to_dict(is_present_values)
        except:
            pass

        # write to a data store
        observation = {
            "name": name,
            "date": date,
            "phase": phase,
            # This bit isn't working
            "is_present": structures.field_value_mapped(
                is_present_field, "", is_present_values
            ),
            "if": string_to_dict(condition, conditional=True),
            "value": value,
            "text": text,
            "occurence_period": occurence_period,
            "context": context,
        }

        optional = ["is_present", "value", "text", "occurence_period", "context"]
        for f in optional:
            if observation[f] == "":
                del observation[f]

        st.session_state.obs_list.append(observation)

# Start printing the currently saved observations in reverse order to that added.
st.write(f"{st.session_state.obs_list}")

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
