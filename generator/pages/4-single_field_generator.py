# single_field_generator.py
# This page will print the toml code for a single field, in the correct format to be read by adtl.

import streamlit as st
import structures
import tomli_w

from webapp import create_field, generate_parser, string_to_dict

st.header("Generate a single parser attribute")
st.write(
    "You can use this page to generate a toml code snippet for a single parser attribute,\
          to copy into a parser you are working on."
)

table = st.text_input("Table", value="subject")
attribute = st.selectbox(
    "Attribute name",
    st.session_state.subject_attributes
    + st.session_state.visit_attributes
    + st.session_state.obs_attributes,
    help="Every attribute option for the subject, visit and obs table is listed here; start typing your attribute name to seach through the list.",
)

# Figure out a way to change the layout here rather than the somewhat restrictive 4 columns; might need to re-do the create_field function for this section
# - but can still reuse a lot of the code.
result = create_field(table, attribute, "")

if st.button("Generate toml snippet", type="primary"):
    toml_snippet = {table: {attribute: result}}

    toml_string = tomli_w.dumps(toml_snippet)

    st.code(toml_string, language="toml")
