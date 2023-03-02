"""
To use, pip install streamlit then run `streamlit run generator/webapp.py` in the terminal.
A locally-hosted website will open in a browser where you can interact with it.
"""

import streamlit as st
import tomli
import tomli_w
import json
import structures
import re

study = {}
subject = {}
visit = {}
observation = {}


@st.cache_data
def string_to_dict(input_string, conditional=False):
    """
    Transforms a comma-seperated string input (e.g. "1=true, 2=false, 3=false")
    into a dictionary with key:value pairs, converts values into appropriate Python types.
    The conditional flag indicates that there may be a conditional rule which needs parsing
    in addition.
    """

    def convert_vals_recursive(res):
        for k, v in res.items():
            try:
                v_converted = json.loads(v)
            except TypeError:  # dict
                v_converted = convert_vals_recursive(v)
            except:
                v_converted = v
            res[k] = v_converted
        return res

    if input_string == "":
        return {}

    if conditional == True:
        result = [re.split("([<>=!]+)", item) for item in input_string.split(", ")]
        for item in result:
            if item[1] == "=":
                del item[1]
            else:
                item[1] = {item[1]: item[2]}
                del item[2]
        result = dict(result)

    else:
        result = dict(item.split("=") for item in input_string.split(", "))

    return convert_vals_recursive(result)


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

            if "," in c_rule:
                error = ValueError(
                    "Only one conditional rule can be entered if a combined option is not selected.\n\
                           Please either change the condition being applied to if.all or if.any, or remove the additional conditions."
                )
                st.exception(error)

            return structures.conditional_field(
                field,
                desc,
                condition,
                string_to_dict(c_rule, conditional=True),
                values_transformed,
            )
        elif condition == "if.any" or condition == "if.all":
            c_rule = col3.text_input(
                "List the conditional rules, e.g. other_cmyn=1, daily+cmyn>=2.",
                key=table + attribute + iterable + "conditionalfield",
            )

            c_rule_transformed = [
                {k: v} for k, v in string_to_dict(c_rule, conditional=True).items()
            ]

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

        st.session_state.toml_dict[table][attribute] = structures.combined_type(
            combination_type, comb_desc, fields
        )

    else:
        columns = st.columns(4)
        st.session_state.toml_dict[table][attribute] = field_types(
            table, attribute, a_type, columns
        )


### -------------------------------------------------------------------------------------
# START STREAMLIT -----------------------------------------------------------------------
### -------------------------------------------------------------------------------------


st.set_page_config(layout="wide")

st.title("Global.health clinical data parser generation")

st.text(
    "This webapp provides semi-automated parser generation for new clinical datasets."
)

st.write(
    "Please use this webapp to auto-generate a .toml parser file.\
    In the sidebar to the left you will find a page for each of the three tables which\
          will be generated: the Subject, Visit and Observations tables.\
    All 3 of these pages will need to be filled in to create a compete parser, which will\
          need checking manually and with the parser validator before being integrated into the ISARIC repository.\n\
    Also provided is a page to generate the toml code for an individual field if you would like to append a small \
        amount of data to an existing toml file while unsure of the syntax."
)


@st.cache_data
def get_attributes_types(table: str):
    with open(f"schemas/dev/{table}.schema.json") as file:
        table_file = json.load(file)

    attributes = list(table_file["properties"].keys())
    required_attributes = table_file["required"]
    attr_types = []
    for v in table_file["properties"].values():
        try:
            attr_types.append(v["type"])
        except KeyError:
            if v["enum"]:
                attr_types.append(v["enum"])
            else:
                attr_types.append(None)

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
# observation, obs_attributes, obs_required_attributes, obs_attr_types = get_attributes_types('observation') # TODO

if "toml_dict" not in st.session_state:
    st.session_state.toml_dict = {}

    with open("generator/base-parser.toml", "rb") as f:
        st.session_state.toml_dict = tomli.load(f)

col1, col2 = st.columns(2)

with col1:
    st.header("Study information")
    parser_name = st.text_input("Parser name:", value="isaric-ccpuk")
    parser_descrip = st.text_input("Parser description", value="ISARIC CCPUK study")
    parser_country = st.text_input("Country code:", value="GBR")
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

with col2:
    st.header("Common mapping types")
    st.write(
        "Use this section to describe common field mappings - e.g., how the form handles yes/no/not known responses."
    )

    # TODO: Date heirarchies for the Observation table aren't included here...

    no_fields = col2.number_input(
        "Number of field mappings to save:",
        value=2,
        key="fieldmapping_numbers",
    )

    refs = []
    map_keys = []
    examples = [
        ["Y/N/NK", "1=true, 2=false, 3=false"],
        [],
        [
            "ethnicity",
            "1=White, 2=Arab, 3=Black, 4=East Asian, 5=South Asian, 6=West Asian, 7=Latin American",
        ],
        [],
    ]

    mf_grid = make_grid(no_fields * 2, 2)

    for i in range(0, no_fields * 2, 2):
        with mf_grid[i][0]:
            refs.append(
                st.text_input(
                    "Mapping reference",
                    value=examples[i][0] if i < len(examples) else "",
                    key="mappingkeyref" + str(i),
                )
            )
        with mf_grid[i][1]:
            map_keys.append(
                st.text_input(
                    "value pairs",
                    value=examples[i][1] if i < len(examples) else "",
                    key="mappingkey" + str(i),
                )
            )

        for square in [
            mf_grid[i + 1][0],
            mf_grid[i + 1][1],
        ]:
            square.markdown("#")

    for r, mk in zip(refs, map_keys):
        st.session_state.toml_dict["adtl"]["defs"][
            r
        ] = structures.predefined_value_maps(string_to_dict(mk))

st.markdown("#")
_, col2, col3, _ = st.columns(4)


def generate_parser(data):
    data["subject"]["subject_id"]["sensitive"] = True
    data["visit"]["subject_id"]["sensitive"] = True
    data["visit"]["visit_id"]["sensitive"] = True

    with open(f"generator/{parser_name}-generator.toml", "wb") as f:
        tomli_w.dump(data, f)
    col2.write("Parser generated! Available in the 'generator' folder.")


if col2.button(
    "Generate Parser", type="primary", use_container_width=True, key="parsergen-home"
):
    generate_parser(st.session_state.toml_dict)
    with open(f"generator/{parser_name}-generator.toml", "rb") as f:
        col3.download_button(
            label="Download Parser",
            data=f,
            file_name=f"{parser_name}.toml",
            use_container_width=True,
        )
