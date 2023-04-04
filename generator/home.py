"""
A new homepage for the graphical interface, integrating the autoparser functionality.
"""

import streamlit as st
import tomli
import json
import pandas as pd
from pathlib import Path
from autoparser.csv_mapping import matches_redcap
from autoparser.make_toml import make_toml

import forms.structures as structures
from forms.structures import string_to_dict


def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")


if "autoparser_df" not in st.session_state:
    st.session_state.autoparser_df = {}
    st.session_state.autoparser_df_checked = {}

if "manual_generation" not in st.session_state:
    st.session_state.manual_generation = False


@st.cache_data
def ap_load_datadict(df):
    """Load the data dictionary into streamlit"""

    with open("autoparser/autoparser/config/redcap-en.toml", "rb") as fp:
        config = tomli.load(fp)
        # this only works if streamlit is run from the root of the isaric repository
        config["schema-path"] = Path.cwd()

    tables = config["schemas"].keys()
    for table in tables:
        df_table = matches_redcap(
            config,
            df,
            table,
            num_matches=6,
        )
        # df.to_csv(f"autoparser-{table}.csv", index=False)
        df_table = df_table.reset_index(drop=True)
        df_table.insert(0, "keep field?", False)
        st.session_state.autoparser_df[table] = df_table


def create_dict():
    with open("autoparser/autoparser/config/redcap-en.toml", "rb") as fp:
        config = tomli.load(fp)
        # this only works if streamlit is run from the root of the isaric repository
        config["schema-path"] = Path.cwd()

    tables = config["schemas"].keys()

    # delete unneeded rows, create the dictionary structure.
    for table in tables:
        st.session_state.autoparser_df_checked[
            table
        ] = st.session_state.autoparser_df_checked[table][
            st.session_state.autoparser_df_checked[table]["keep field?"]
        ]
        st.session_state.autoparser_df_checked[table].drop(columns=["keep field?"])

    mappings = pd.concat(
        (st.session_state.autoparser_df_checked[table] for table in tables),
        ignore_index=True,
    )

    if "toml_dict" not in st.session_state:
        st.session_state.toml_dict = {}

    st.session_state.toml_dict = make_toml(config, mappings, "isaric")


st.set_page_config(layout="wide")

st.title("Global.health clinical data parser generation")

if st.session_state.manual_generation is False:
    st.write(
        "This webapp provides semi-automated parser generation for new clinical\
            datasets."
    )

    st.write(
        "To start, please upload the data dictionary (NOT THE RAW DATA FILE) as a csv\
        file using the button below."
    )
    st.write(
        "If you don't have a data dictionary, or the dictionary is in a different file\
        format (we are working on adding functionality for pdf data dictionaries)\
        please click the 'Contine to manual parser generation' button to add each data\
        field by hand.\
        "
    )

    _, col1, col2, _ = st.columns(4)

    ap_file = col1.file_uploader("Upload data dictionary", type=["csv"])
    st.session_state.manual_generation = col2.button(
        "Continue to manual parser generation", use_container_width=True, type="primary"
    )
    if ap_file is not None:

        @st.cache_data
        def uploaded_dd():
            ap_df = pd.read_csv(ap_file)
            parser = json.load(open("schemas/dev/parser.schema.json"))
            st.session_state.parser = parser

            return ap_df

        df = uploaded_dd()
        ap_load_datadict(df)
    elif st.session_state.manual_generation is True:
        st.experimental_rerun()

if "subject" in st.session_state.autoparser_df:
    st.write(
        "Thank you for uploading your data dictionary.\n\
        Below is a set of auto-generated suggestions for mapping data fields to\
        attributes.\n\
        Select those that are correct (or the closest option) using the checkboxes in\
        the 'keep field?' column.\n\
        If none of the options provided are a close match to the real mapping,\
        leave all the attribute mappings unchecked; equally, if more than one field is\
        relevent, mark all the relevent fields for an attribute.\n\
        At the next stage, those attributes with multiple fields checked will be\
        combined, and you will be able to edit and add entries."
    )

    st.write(
        "Each table can be expanded to be viewed in fullscreen mode using the toggle to\
        the right. Once all three tables have been viewed and selections have been made\
        , click the 'Next' button to load the suggestions into the graphical interface."
    )

    st.header("Subject")
    st.session_state.autoparser_df_checked["subject"] = st.experimental_data_editor(
        st.session_state.autoparser_df["subject"],
        use_container_width=True,
    )

    st.header("Visit")
    st.session_state.autoparser_df_checked["visit"] = st.experimental_data_editor(
        st.session_state.autoparser_df["visit"],
        use_container_width=True,
    )

    st.header("Observations")
    st.session_state.autoparser_df_checked["observation"] = st.experimental_data_editor(
        st.session_state.autoparser_df["observation"],
        use_container_width=True,
    )

    _, col, _ = st.columns([1, 2, 1])
    dict_created = col.button(
        "Next", type="primary", use_container_width=True, on_click=create_dict
    )

    if dict_created:
        pass
    # go to the subject page to view the subject parser table.

if st.session_state.manual_generation is True:
    st.write(
        "In the sidebar to the left you will find a page for each of the three\
    tables which will be generated: the Subject, Visit and Observations\
    tables."
    )
    st.write(
        "All 3 of these pages need filling in to create a complete parser, which will\
    need checking manually and with the parser validator before being integrated into\
    the ISARIC repository."
    )
    st.write(
        "If you would like to write the parser directly, the `base-parser.toml`\
     file contains all the headers for the subject and visit tables, which can\
     be filled in as required, along with an example of how the 'observations'\
     should be formatted."
    )
    st.write(
        "Also provided is a page to generate the toml code for an individual field\
     if you would like write to the toml file directly but are unsure of the\
     syntax. This code can be copied and pasted into your parser file.\
    "
    )

    @st.cache_data
    def get_attributes_types(table: str):
        with open(f"schemas/dev/{table}.schema.json") as file:
            table_file = json.load(file)

        attributes = list(table_file["properties"].keys())
        required_attributes = table_file["required"]
        attr_types = {}
        for k, v in table_file["properties"].items():
            try:
                attr_types[k] = v["type"]
            except KeyError:
                if v["enum"]:
                    attr_types[k] = v["enum"]
                else:
                    attr_types[k] = None

        return table_file, attributes, required_attributes, attr_types

    (
        st.session_state.subject,
        st.session_state.subject_attributes,
        st.session_state.subject_required_attributes,
        st.session_state.subject_attr_types,
    ) = get_attributes_types("subject")
    (
        st.session_state.visit,
        st.session_state.visit_attributes,
        st.session_state.visit_required_attributes,
        st.session_state.visit_attr_types,
    ) = get_attributes_types("visit")
    (
        st.session_state.obs,
        st.session_state.obs_attributes,
        st.session_state.obs_required_attributes,
        st.session_state.obs_attr_types,
    ) = get_attributes_types("observation")

    if "toml_dict" not in st.session_state:
        st.session_state.toml_dict = {}

        with open("generator/base-parser-empty.toml", "rb") as f:
            st.session_state.toml_dict = tomli.load(f)

        parser = json.load(open("schemas/dev/parser.schema.json"))
        st.session_state.parser = parser

    st.markdown("#### Study information:")
    col1, col2, col3 = st.columns(3)
    with col1:
        parser_name = st.text_input(
            "Parser name:", value="isaric-ccpuk"
        )  # dev note: change to placeholder once testing is complete
    with col2:
        parser_descrip = st.text_input("Parser description", value="ISARIC CCPUK study")
    with col3:
        pathogen = st.text_input("Pathogen under study:", value="COVID-19")

    st.session_state.toml_dict["adtl"]["name"] = parser_name
    st.session_state.toml_dict["adtl"]["description"] = parser_descrip

    st.session_state.toml_dict["study"]["id"] = parser_name

    st.session_state.toml_dict["subject"]["study_id"] = parser_name
    st.session_state.toml_dict["subject"]["pathogen"] = pathogen

    V_SPACE(1)

    st.markdown("### Pre-defined value maps")
    st.write(
        "In many cases, a parser attribute will require a value map which is repeated\
        in multiple other attributes."
    )
    st.write(
        "For example, questions where the response can be either 'Yes', 'No' or\
        'Unknown' are frequent throughout most clinical data forms, and responses will\
        usually be stored the same way across a single study database (e.g. 1=yes, 0=no\
        , 2=unknown)."
    )
    st.write(
        "To avoid repeated code and unnecessary extra typing, a single value map\
        can be referred to throughout the parser by pre-defining the map.\
        "
    )
    st.write(
        "Value maps used in the CCPUK study have been pre-loaded as an example below."
    )
    st.write(
        "To edit the existing entries, or add a new one, use the form to the right.\
        If a reference which already exists, e.g. 'Y/N/NK' is given as the\
        reference in the form, the current map will be overwritten."
    )

    col1, col2 = st.columns(2)

    with col1:
        # show a json file for the current mappings
        st.json(st.session_state.toml_dict["adtl"]["defs"])

    with col2:
        st.markdown("#### Add or edit a reference map:")
        mapping_ref = st.text_input(
            "Mapping reference",
            placeholder="Y/N/NK",
        )

        multifield_mapping = st.checkbox("Are there multiple fields to combine?")
        if multifield_mapping:
            subcol1, subcol2 = st.columns(2)
            combination_type = subcol1.selectbox(
                "Which combined type?",
                ["any", "all", "firstNonNull", "list", "set"],
                key="MappingscombinationType",
            )
            no_fields = subcol2.number_input(
                "How many fields are there to combine?", value=2
            )

            st.markdown("#### Fields to combine:")

            fields = structures.value_map_multi(no_fields)

        else:
            value_field = st.text_area(
                "Value map",
                key="keymaps_values",
                placeholder="2=slight, 3=moderate, 4=severe, 5=unable",
            )

        if st.button("Upload edits to reference maps", type="primary"):
            if multifield_mapping:
                st.session_state.toml_dict["adtl"]["defs"][
                    mapping_ref
                ] = structures.combined_type(combination_type, "", fields)
            else:
                st.session_state.toml_dict["adtl"]["defs"][mapping_ref] = {
                    "values": string_to_dict(value_field)
                }
            st.experimental_rerun()
