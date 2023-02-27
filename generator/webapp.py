"""
To use, pip install streamlit then run `streamlit run generator/webapp.py` in the terminal.
A locally-hosted website will open in a browser where you can interact with it.
"""

import streamlit as st
import tomli
import tomli_w
import json
import structures

study = {}
subject = {}
visit = {}
observation = {}


def string_to_dict(input_string):
    """
    Transforms a comma-seperated string input (e.g. "1=true, 2=false, 3=false")
    into a dictionary with key:value pairs, converts values into appropriate Python types.
    """
    if input_string == "":
        return {}

    try:
        result = dict(item.split("=") for item in input_string.split(", "))
    except:
        dict(input_string.split("="))
    for k, v in result.items():
        try:
            v_converted = json.loads(v)
        except:
            v_converted = v
        result[k] = v_converted

    return result


def make_grid(cols, rows):
    # creates a grid layout in streamlit
    grid = [0] * cols
    for i in range(cols):
        with st.container():
            grid[i] = st.columns(rows)
    return grid


def field_types(table, attribute, a_type, columns, iterable="0"):
    col0, col1, col2, col3 = columns

    if a_type == "boolean" or type(a_type) == list:
        i = 1
        if type(a_type) == list:
            optional_vals = ", ".join([f"{i+1}={v}" for i, v in enumerate(a_type)])
        else:
            optional_vals = "Y/N/NK"
    else:
        i = 0
        optional_vals = None

    input_type = col1.selectbox(
        "Type of input field",
        [
            "single field",
            "field with value mapping",
            "single field with conditional",
            "value mapped with conditional",
            "date field",
            "field with units",
            "applying a data transformation",
        ],
        key=table + attribute + iterable + "type",
        index=i,
    )

    field = col2.text_input(
        "Field (column) name", key=table + attribute + iterable + "field"
    )
    desc = col2.text_input("Description", key=table + attribute + iterable + "desc")

    if input_type == "single field":
        return structures.single_field(field, desc)

    elif input_type == "field with value mapping":
        col3.write(
            "Value maps can be given either as e.g., '1=alive, 2=hospitalised, 3=death, ...'"
        )
        col3.write(
            "or as a reference to a predefined mapping given in the top section, e.g., 'Y/N/NK'."
        )
        values = col3.text_input(
            "Value mapping given as, e.g., 1=alive, 2=hospitalised, 3=death",
            key=table + attribute + iterable + "valuemap",
            value=optional_vals,
        )
        try:
            values_transformed = string_to_dict(values)
            return structures.field_value_mapped(field, desc, values_transformed)
        except:
            return structures.field_value_mapped(field, desc, values)

    elif "with conditional" in input_type:
        if input_type == "value mapped with conditional":
            values = col2.text_input(
                "Value mapping given as, e.g., 1=alive, 2=hospitalised, 3=death, or refer to predefined maps e.g.Y/N/NK",
                key=table + attribute + iterable + "valuemap",
                value=optional_vals,
            )
            try:
                values_transformed = string_to_dict(values)
            except:
                values_transformed = values
        else:
            values_transformed = None

        condition = col3.selectbox(
            "The condition to be applied",
            ["if", "if.all", "if.any"],
            key=table + attribute + iterable + "if",
        )
        if condition == "if":
            c_rule = col3.text_input(
                "The conditional rule, e.g. other_cmyn=1, with no spaces.",
                key=table + attribute + iterable + "conditionalfield",
            )

            return structures.conditional_field(
                field, desc, condition, string_to_dict(c_rule), values_transformed
            )
        elif condition == "if.any" or condition == "if.all":
            no_conditions = col3.number_input(
                "How many fields are there to combine?", value=2
            )
            c_rule = []

            for i in range(no_conditions):
                c_rule.append(
                    col3.text_input(
                        "The conditional rule, e.g. other_cmyn=1, with no spaces.",
                        key=table + attribute + iterable + "conditionalfield" + str(i),
                    )
                )

            c_rule_transformed = [string_to_dict(rule) for rule in c_rule]

            return structures.conditional_field(
                field, desc, condition, c_rule_transformed, values_transformed
            )

    elif input_type == "date field":
        source_date = col3.text_input(
            "Source date format",
            value="%d/%m/%Y",
            key=table + attribute + iterable + "sourcedate",
        )
        return structures.field_with_date(field, desc, source_date)

    elif input_type == "field with units":
        unit = col3.text_input(
            "Desired output unit", value="kg", key=table + attribute + iterable + "unit"
        )
        source_unit = col3.text_input(
            "Field name for source unit",
            key=table + attribute + iterable + "sourceunit",
        )
        source_values = col3.text_input(
            "Value mapping for units",
            value="1=kg, 2=lb",
            key=table + attribute + iterable + "sourcevalue",
        )
        values = string_to_dict(source_values)

        return structures.field_with_unit(field, desc, unit, source_unit, values)

    elif input_type == "applying a data transformation":
        apply = col3.selectbox(
            "The transformation to be applied",
            ["isNotNull", "yearsElapsed"],
            key=table + attribute + iterable + "apply",
        )
        params = col3.text_input(
            "Parameter fields required by the transformation (optional)",
            key=table + attribute + iterable + "applyparam",
        )

        if params == "":
            params = None

        return structures.field_with_transformation(field, desc, apply, params)


def create_field(table, attribute, a_type):
    col0, col1, col2, col3 = st.columns(4)
    if col1.checkbox("Multiple fields to combine?", key=table + attribute + "combine"):
        combination_type = col1.selectbox(
            "Which combined type should be applied?",
            ["any", "all", "firstNonNull", "list"],
            key=table + attribute + "combinationType",
        )
        comb_desc = col1.text_input(
            "Description", key=table + attribute + "combinationdesc"
        )
        no_fields = col1.number_input(
            "How many fields are there to combine?",
            value=2,
            key=table + attribute + "multifield",
        )

        fields = []

        mf_grid = make_grid(no_fields * 2, 4)

        for i in range(0, no_fields * 2, 2):
            columns = mf_grid[i][0], mf_grid[i][1], mf_grid[i][2], mf_grid[i][3]
            field = field_types(table, attribute, a_type, columns, iterable=str(i))
            fields.append(field)
            for square in [
                mf_grid[i + 1][0],
                mf_grid[i + 1][1],
                mf_grid[i + 1][2],
                mf_grid[i + 1][3],
            ]:
                square.markdown("#")

        toml_dict[table][attribute] = structures.combined_type(
            combination_type, comb_desc, fields
        )

    else:
        columns = st.columns(4)
        toml_dict[table][attribute] = field_types(table, attribute, a_type, columns)


st.set_page_config(layout="wide")

st.title("Global.health clinical data parser generation")

st.text(
    "This webapp provides semi-automated parser generation for new clinical datasets."
)

st.write(
    "Please fill in the form below to auto-generate a .toml parser file. This will need checking manually before being integrated into the ISARIC repository."
)

# Get the possible attributes for each table from existing schemas
# If this is the only schema we're planning on having, this option is redundant
schema = st.selectbox("Choose a schema to base your parser from.", ["ISARIC"])

# link the schema name to the folder it's located in
schema_folder = {"ISARIC": "dev"}
f_sub = open(f"schemas/{schema_folder[schema]}/subject.schema.json")
subject = json.load(f_sub)
subject_attributes = list(subject["properties"].keys())
subject_attr_types = []
for v in subject["properties"].values():
    try:
        subject_attr_types.append(v["type"])
    except KeyError:
        if v["enum"]:
            subject_attr_types.append(v["enum"])
        else:
            subject_attr_types.append(None)


f_visit = open(f"schemas/{schema_folder[schema]}/visit.schema.json")
visit = json.load(f_visit)
visit_attributes = list(visit["properties"].keys())
visit_attr_types = []
for v in visit["properties"].values():
    try:
        visit_attr_types.append(v["type"])
    except KeyError:
        if v["enum"]:
            visit_attr_types.append(v["enum"])
        else:
            visit_attr_types.append(None)

# TODO: Auto-generate observation section.
# f_obs = open(f"schemas/{schema_folder[schema]}/observation.schema.json")
# observation = json.load(f_obs)
# obs_attributes = list(subject["properties"].keys())

with open("generator/base-parser.toml", "rb") as f:
    toml_dict = tomli.load(f)

    col1, col2 = st.columns(2)

    with col1:
        st.header("Study information")
        parser_name = st.text_input("Parser name:", value="isaric-ccpuk")
        parser_descrip = st.text_input("Parser description", value="ISARIC CCPUK study")
        parser_country = st.text_input("Country code:", value="GBR")
        study_date = st.text_input("Study date:", value="2021-01-01")
        pathogen = st.text_input("Pathogen under study:", value="COVID-19")

    toml_dict["adtl"]["name"] = parser_name
    toml_dict["adtl"]["description"] = parser_descrip

    toml_dict["study"]["id"] = parser_name
    toml_dict["study"]["date"] = study_date
    toml_dict["study"]["country_iso3"] = parser_country

    toml_dict["subject"]["study_id"] = parser_name
    toml_dict["subject"]["country_iso3"] = parser_country
    toml_dict["subject"]["pathogen"] = pathogen

    with col2:
        st.header("Common mapping types")
        st.write(
            "Use this section to describe common field mappings - e.g., how the form handles yes/no/not known responses."
        )

        # TODO: need to be able to loop through and add more of these
        subcol1, subcol2 = st.columns(2)
        with subcol1:
            ref = st.text_input("Mapping reference", value="Y/N/NK")

        with subcol2:
            map_key = st.text_input("value pairs", value="1=true, 2=false, 3=false")

        toml_dict["adtl"]["defs"][ref] = structures.predefined_value_maps(
            string_to_dict(map_key)
        )

with open(f"generator/{parser_name}.toml", "wb") as f:
    tomli_w.dump(toml_dict, f)

st.markdown(
    """<hr style="height:5px;border:none;color:#333;background-color:#333;" /> """,
    unsafe_allow_html=True,
)

with st.expander("subjects table"):
    st.header("Subject table")
    st.write(
        f"All the available mapping fields (based on the {schema} schema) for the subject field are listed below."
    )
    st.write(
        "If a given field has a corresponding column in your form, check the box next to it and the section will expand to be filled."
    )
    with open(f"generator/{parser_name}.toml", "rb") as f:
        toml_dict = tomli.load(f)

    for attribute, s_type in zip(subject_attributes, subject_attr_types):
        if st.checkbox(attribute, key="subject" + attribute + "selectbox"):
            create_field("subject", attribute, s_type)
        st.markdown(
            """<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """,
            unsafe_allow_html=True,
        )

with st.expander("visit table"):
    st.header("Visit table")
    st.write(
        "All the available mapping fields (based on the ISARIC schema) for the visit field are listed below."
    )
    st.write(
        "If a given field has a corresponding column in your form, check the box next to it and the section will expand to be filled."
    )

    for attribute, a_type in zip(visit_attributes, visit_attr_types):
        if st.checkbox(attribute, key="visit" + attribute + "selectbox"):
            create_field("visit", attribute, a_type)
        st.markdown(
            """<hr style="height:2px;border:none;color:#333;background-color:#333;" /> """,
            unsafe_allow_html=True,
        )

_, col2, col3, _ = st.columns(4)


def generate_parser(data):
    with open(f"generator/{parser_name}.toml", "wb") as f:
        tomli_w.dump(data, f)
    col2.write("Parser generated! Available in the 'generator' folder.")


if col2.button("Generate Parser", type="primary", use_container_width=True):
    generate_parser(toml_dict)
    with open(f"generator/{parser_name}.toml", "rb") as f:
        col3.download_button(
            label="Download Parser",
            data=f,
            file_name=f"{parser_name}.toml",
            use_container_width=True,
        )
