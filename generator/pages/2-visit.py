# visit.py
# stores the visit table page

import streamlit as st
import tomli
import tomli_w
import json
import structures
import re

from webapp import create_field, generate_parser

st.header("Visit table")
st.write(
    "All the available mapping fields (based on the ISARIC schema) for the visit table are listed below. \
        Constant fields will be taken automatically from the study-level table above."
)
st.write(
    "If a given field has a corresponding column in your form, check the box next to it and the section will expand to be filled."
)
st.write(
    "If a given field is auto-expanded and not clickable, the field is required and must be filled in.\n\
        Contact the developers if your CRF does not have this field!"
)
st.markdown("#")

constant_attrs = ["country_iso3"]
for attribute, a_type in zip(
    st.session_state.visit_attributes, st.session_state.visit_attr_types
):
    if attribute in constant_attrs:
        continue
    elif attribute in st.session_state.visit_required_attributes:
        st.write("☑️", attribute)
        st.session_state.toml_dict["visit"][attribute] = create_field(
            "visit", attribute, a_type
        )
    elif st.checkbox(attribute, key="visit" + attribute + "selectbox"):
        st.session_state.toml_dict["visit"][attribute] = create_field(
            "visit", attribute, a_type
        )
    st.markdown(
        """<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """,
        unsafe_allow_html=True,
    )

_, col2, col3, _ = st.columns(4)

parser_name = st.session_state.toml_dict["adtl"]["name"]

if col2.button(
    "Generate Parser", type="primary", use_container_width=True, key="parsergen-visit"
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
