# subject.py
# Stores the subject table

import streamlit as st

from webapp import generate_parser
from forms.visit_subject import create_field
from forms.view_table import view_parser
from forms.structures import sidebar_search, V_SPACE

subject_attributes = st.session_state.parser["properties"]["subject"][
    "properties"
].keys()
required_attributes = st.session_state.parser["properties"]["subject"]["required"]

with st.sidebar:
    sidebar_search("subject")


st.header("Subject table")

st.write(
    "The 'attribute name' dropdown box contains all the available mapping fields within\
          the current schema, for the subject table. Constant fields will be taken from\
          the study-level table on the [home page](home)."
)
if st.session_state.manual_generation:
    st.write(
        "As each attribute is added, you will see the table at the bottom of the page\
        fill out with the added attributes and their corresponding mapping. If you want\
        to change an attribute map, re-do the form and the row(s) will be replaced."
    )
else:
    st.write(
        "The table below is currently filled with the 'subject' attributes you selected\
        with the autoparser functionality. You can edit the auto-generated entries,\
        or add new attributes, by selecting from the drop-down 'attribute name' box.\
        Where an attribute already exists, the form will be pre-filled with\
        existing data, which can be edited. Once you're happy, click 'Apply this\
        attribute' to save your changes."
    )

st.write(
    "When you have filled in the subject, visit and observation pages, click 'Generate\
        Parser' (found at the bottom of each page) to generate a parser .toml file\
              ready for use."
)

# st.write("We strongly advise you to check and validate the parser (see [docs]
# (https://github.com/globaldothealth/isaric/blob/mapping-guide/docs/guide.md)\
#          before use to catch any breaking errors.)")
V_SPACE(1)

# constant_attrs = ["study_id", "country_iso3", "pathogen"]

cola, colb = st.columns(2)
attribute = cola.selectbox("Attribute name", subject_attributes)

if attribute in st.session_state.toml_dict["subject"]:
    current_data = st.session_state.toml_dict["subject"][attribute]
    if "fields" in current_data:
        mf = True
    else:
        mf = False
else:
    current_data, mf = False, False

colb.markdown("#")
multifields = colb.checkbox("Multiple fields to combine?", value=mf)
st.markdown("#")

# if attribute in constant_attrs:
#     st.write(
#         "This is a constant attribute.\
#               If you wish to edit it, please use the webapp home page."
#     )
# else:
# This will also allow overwriting if present.
field = create_field(
    "subject",
    attribute,
    st.session_state.subject_attr_types[attribute]
    if "subject_attr_types" in st.session_state
    else "",
    multifields,
    data_provided=current_data,
)

col1, col2, col3 = st.columns(3)
if col2.button("Apply this attribute to the table", type="primary"):
    st.session_state.toml_dict["subject"][attribute] = field

st.markdown("### Attributes currently in the 'subject' table")

if not all(
    x in st.session_state.toml_dict["subject"].keys() for x in required_attributes
):
    missing_fields = [
        attr
        for attr in required_attributes
        if attr not in st.session_state.toml_dict["subject"].keys()
    ]
    st.warning(
        f"You are missing the following required attributes from the Subject\
              table: {missing_fields}"
    )

# st.dataframe(
#     view_parser(
#         st.session_state.toml_dict["subject"], constant_attrs, reverse_order=True
#     ),
# )
st.dataframe(
    view_parser(
        st.session_state.toml_dict["subject"],
        ["study_id", "pathogen"],
        reverse_order=True,
    ),  # ideally only  reverse the order when data isn't being provided.
)

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
