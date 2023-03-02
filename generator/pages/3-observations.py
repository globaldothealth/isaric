# observations.py

import streamlit as st
import tomli
import tomli_w
import json
import structures
import re

from webapp import create_field, generate_parser

st.header("Observations table")
st.write(
    "All the available mapping fields (based on the ISARIC schema) for the observations table are listed below. \
        Constant fields will be taken automatically from the study-level table on the home page."
)
st.write(
    "If a given field has a corresponding column in your form, check the box next to it and the section will expand to be filled."
)
st.write(
    "If a given field is auto-expanded and not clickable, the field is required and must be filled in.\n\
        Contact the developers if your CRF does not have this field!"
)
st.markdown("#")
