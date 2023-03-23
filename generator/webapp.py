"""
To use, pip install streamlit then run `streamlit run generator/webapp.py` in
the terminal. A locally-hosted website will open in a browser where you can
interact with it.
"""

import streamlit as st
import tomli
import tomli_w
import json
import forms.structures as structures

from forms.structures import string_to_dict, make_grid

study = {}
subject = {}
visit = {}
observation = {}


def validate_required_fields(data):
    # currently only validates subject and visit required fields are present
    missing_fields_sub = []
    for field in st.session_state.subject_required_attributes:
        if field not in data["subject"]:
            missing_fields_sub.append(field)
        elif data["subject"][field] != "":
            pass
        elif data["subject"][field] == "":
            missing_fields_sub.append(field)
        elif data["subject"][field]["field"] == "":
            missing_fields_sub.append(field)

    missing_fields_visit = []
    for field in st.session_state.visit_required_attributes:
        if field not in data["visit"]:
            missing_fields_visit.append(field)
        elif data["visit"][field] != "":
            pass
        elif data["visit"][field] == "":
            missing_fields_visit.append(field)
        elif data["visit"][field]["field"] == "":
            missing_fields_visit.append(field)

    if len(missing_fields_sub + missing_fields_visit) > 0:
        st.error(
            f"There are required fields missing from the subject or visit\
                 tables.\n\
                Subject: {missing_fields_sub}\n\
                 Visit: {missing_fields_visit}"
        )
        return False

    return True


def generate_parser(data):
    if validate_required_fields(data):
        data["subject"]["subject_id"]["sensitive"] = True
        data["visit"]["subject_id"]["sensitive"] = True
        data["visit"]["visit_id"]["sensitive"] = True

        if "obs_list" not in st.session_state:
            st.warning("Your parser doesn't contain any observations at the moment!")

        else:
            for obs in st.session_state.obs_list:
                if "observation" in data.keys():
                    overwrite = False
                    # check whether an observation previously existed
                    for i, d in enumerate(data["observation"]):
                        if d["name"] == obs["name"] and d["phase"] == obs["phase"]:
                            data["observation"][i] = obs
                            overwrite = True
                            break

                    if overwrite is False:
                        data["observation"].append(obs)
                else:
                    data["observation"] = [obs]

        with open(f"generator/{parser_name}-generator.toml", "wb") as f:
            tomli_w.dump(data, f)

        return True
    return False


# -----------------------------------------------------------------------------
# START STREAMLIT -------------------------------------------------------------
# -----------------------------------------------------------------------------


st.set_page_config(layout="wide")

st.title("Global.health clinical data parser generation")

st.write(
    "This webapp provides semi-automated parser generation for new clinical datasets."
)

st.write(
    "Please use this webapp to auto-generate a .toml parser file.\
    In the sidebar to the left you will find a page for each of the three\
     tables which will be generated: the Subject, Visit and Observations\
     tables. All 3 of these pages will need to be filled in to create a\
     complete parser, which will need checking manually and with the parser\
     validator before being integrated into the ISARIC repository.\n\
    If you would like to write the parser directly, the `base-parser.toml`\
     file contains all the headers for the subject and visit tables, which can\
     be filled in as required, along with an example of how the 'observations'\
     should be formatted.\n\
    Also provided is a page to generate the toml code for an individual field\
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

st.header("Study information")
col1, col2 = st.columns(2)
with col1:
    parser_name = st.text_input("Parser name:", value="isaric-ccpuk")
    parser_descrip = st.text_input("Parser description", value="ISARIC CCPUK study")
    parser_country = st.text_input("Country code:", value="GBR")
with col2:
    study_date = st.text_input("Study date:", value="2021-01-01")
    pathogen = st.text_input("Pathogen under study:", value="COVID-19")

st.session_state.toml_dict["adtl"]["name"] = parser_name
st.session_state.toml_dict["adtl"]["description"] = parser_descrip

st.session_state.toml_dict["study"]["id"] = parser_name
st.session_state.toml_dict["study"]["date"] = study_date
st.session_state.toml_dict["study"]["country_iso3"] = parser_country

st.session_state.toml_dict["subject"]["study_id"] = parser_name
st.session_state.toml_dict["subject"]["country_iso3"] = parser_country
st.session_state.toml_dict["subject"]["pathogen"] = pathogen

st.session_state.toml_dict["visit"]["country_iso3"] = parser_country


st.markdown("#")

st.header(
    "Below are the common mapping types for value fields currently defined in\
          the parser file."
)
st.write(
    "To edit the existing maps, or add a new one, use the form to the right.\
     If a reference which already exists, e.g. 'Y/N/NK' is given as the\
     reference in the form, the current map will be overwritten."
)

col1, col2 = st.columns(2)

with col1:
    # show a json file for the current mappings
    st.json(st.session_state.toml_dict["adtl"]["defs"])

with col2:
    st.markdown("### Add or edit a reference map:")
    mapping_ref = st.text_input("Mapping reference", placeholder="Y/N/NK")

    multifield_mapping = st.checkbox("Are there multiple fields to combine?")
    if multifield_mapping:
        subcol1, subcol2 = st.columns(2)
        combination_type = subcol1.selectbox(
            "Which combined type should be applied?",
            ["any", "all", "firstNonNull", "list"],
            key="MappingscombinationType",
        )
        no_fields = subcol2.number_input(
            "How many fields are there to combine?", value=2
        )
        fields = []

        st.markdown("#### Fields to combine:")

        mf_grid = make_grid(no_fields * 2, 2)

        for i in range(0, no_fields * 2, 2):
            cell1, cell2 = mf_grid[i][0], mf_grid[i][1]
            with cell1:
                field_name = st.text_input(
                    f"Field name ({i})", key="keymaps_fields" + str(i)
                )
                st.markdown("#")
                st.markdown("###")
                descrip = st.text_input(
                    "Description (optional)", key="keymaps_description" + str(i)
                )
            with cell2:
                val_map = st.text_area(
                    "Value map (optional)",
                    key="keymaps_values" + str(i),
                    placeholder="2=slight, 3=moderate, 4=severe, 5=unable",
                )
                conditional = st.text_input(
                    "Condition (optional)",
                    key="keymaps_condition" + str(i),
                    placeholder="dsterm=4",
                )
            if conditional != "":
                if val_map != "":
                    fields.append(
                        structures.conditional_field(
                            field_name,
                            descrip,
                            "if",
                            string_to_dict(conditional, conditional=True),
                            values=string_to_dict(val_map),
                        )
                    )
                else:
                    fields.append(
                        structures.conditional_field(
                            field_name,
                            descrip,
                            "if",
                            string_to_dict(conditional, conditional=True),
                        )
                    )
            elif val_map != "":
                fields.append(
                    structures.field_value_mapped(
                        field_name,
                        descrip,
                        values=string_to_dict(val_map),
                    )
                )
            else:
                fields.append(structures.single_field(field_name, descrip))

            for square in [
                mf_grid[i + 1][0],
                mf_grid[i + 1][1],
            ]:
                square.markdown("#")
                square.markdown("#")
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
