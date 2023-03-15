# subject.py
# Stores the subject table

import streamlit as st
import pandas as pd

from webapp import generate_parser
from forms.visit_subject import create_field

st.header("Subject table")
st.write(
    f"All the available mapping fields (based on the ISARIC schema) for the subject table are listed below. \
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

constant_attrs = ["study_id", "country_iso3", "pathogen"]

cola, colb = st.columns(2)
attribute = cola.selectbox("Attribute name", st.session_state.subject_attributes)
colb.markdown("#")
multifields = colb.checkbox("Multiple fields to combine?")
st.markdown("#")

if attribute in constant_attrs:
    st.write(
        "This is a constant attribute. If you wish to edit it, please use the webapp home page."
    )
else:
    # This will also allow overwriting if present.
    field = create_field(
        "subject",
        attribute,
        st.session_state.subject_attr_types[attribute],
        multifields,
    )

    col1, col2, col3 = st.columns(3)
    if col2.button("Apply this attribute to the table", type="primary"):
        st.session_state.toml_dict["subject"][attribute] = field

if not all(
    x in st.session_state.toml_dict["subject"].keys()
    for x in st.session_state.subject_required_attributes
):
    missing_fields = [
        attr
        for attr in st.session_state.subject_required_attributes
        if attr not in st.session_state.toml_dict["subject"].keys()
    ]
    st.warning(
        f"You are missing the following required attributes from the Subject table: {missing_fields}"
    )

df = pd.DataFrame.from_dict(
    st.session_state.toml_dict["subject"],
    orient="index",
    columns=["values"],
)
st.table(df)

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
