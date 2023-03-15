# visit.py
# stores the visit table page

import streamlit as st
import pandas as pd

from webapp import generate_parser
from forms.visit_subject import create_field

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

cola, colb = st.columns(2)
attribute = cola.selectbox("Attribute name", st.session_state.visit_attributes)
colb.markdown("#")
multifields = colb.checkbox(
    "Multiple fields to combine?", key="visit_multifield_checkbox"
)
st.markdown("#")

if attribute in constant_attrs:
    st.write(
        "This is a constant attribute. If you wish to edit it, please use the webapp home page."
    )
else:
    # This will also allow overwriting if present.
    field = create_field(
        "visit", attribute, st.session_state.visit_attr_types[attribute], multifields
    )

    col1, col2, col3 = st.columns(3)
    if col2.button("Apply this attribute to the table", type="primary"):
        st.session_state.toml_dict["visit"][attribute] = field

if not all(
    x in st.session_state.toml_dict["visit"].keys()
    for x in st.session_state.visit_required_attributes
):
    missing_fields = [
        attr
        for attr in st.session_state.visit_required_attributes
        if attr not in st.session_state.toml_dict["visit"].keys()
    ]
    st.warning(
        f"You are missing the following required attributes from the Visit table: {missing_fields}"
    )

df = pd.DataFrame.from_dict(
    st.session_state.toml_dict["visit"],
    orient="index",
    columns=["values"],
)
st.table(df)

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
