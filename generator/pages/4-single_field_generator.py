# single_field_generator.py
# This page will output the toml code for a single field, in the correct format to be read by adtl.

import streamlit as st
import tomli_w

from forms.observation import observation_form
from forms.visit_subject import create_field

if "single_field_observation" not in st.session_state:
    st.session_state.single_field_observation = {}

st.header("Generate a single parser attribute")
st.write(
    "You can use this page to generate a toml code snippet for a single parser attribute,\
          to copy into a parser you are working on."
)

table = st.selectbox("Table", ["subject", "visit", "observation"])

if table == "observation":
    obs = observation_form("Click here to compile the observation", False)
    if obs is not None:
        st.session_state.single_field_observation = obs
else:
    attribute = st.selectbox(
        "Attribute name",
        st.session_state.subject_attributes
        + st.session_state.visit_attributes
        + st.session_state.obs_attributes,
        help="Every attribute option for the subject, visit and obs table is listed here; start typing your attribute name to seach through the list.",
    )
    result = create_field(table, attribute, "", [0.1, 1, 1, 1])

if st.button("Generate toml snippet", type="primary"):
    if table == "observation":
        toml_snippet = {table: [st.session_state.single_field_observation]}
    else:
        toml_snippet = {table: {attribute: result}}

    toml_string = tomli_w.dumps(toml_snippet)

    st.code(toml_string, language="toml")
    st.markdown("#### Please Note:")
    st.write(
        "This page will produce a toml snippet with all tables fully expanded.\
             If you wish to condense the entry, note that"
    )
    st.code(
        """
        [[observation]]
        name = "pao2"

        [observation.text]
        field = 'daily_pao2_lborres'

        [observation.text.values]
        1 = "Arterial"
        2 = "Venous"
        3 = "Capillary"
            """,
        language="toml",
    )
    st.write(" is equivalent to")
    st.code(
        """
        [[observation]]
        name = "pao2"
        text = {field = 'daily_pao2_lborres', values = { 1 = "Arterial", 2 = "Venous", 3 = "Capillary" }}.""",
        language="toml",
    )
    st.write(
        "We suggest condensing short tables as above where sensible to reduce the length and increase readability of parser files."
    )
