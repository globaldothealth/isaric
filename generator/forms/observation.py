import streamlit as st
import forms.structures as structures

from forms.structures import string_to_dict


def observation_form(button_label, clear_on_sub):
    with st.form(key="observation", clear_on_submit=clear_on_sub):
        st.write("Required fields:")
        (
            col1,
            col2,
        ) = st.columns(2)
        with col1:
            name = st.selectbox(
                "Observation name", st.session_state.obs["properties"]["name"]["enum"]
            )
            phase = st.radio(
                "Observation phase", ["admission", "study", "followup"], horizontal=True
            )
        with col2:
            date = st.text_input(
                "Date of observation",
                value="admissionDateHierarchy",
                help="This can either be a single field name where the date is stored,\
                                or a reference to a pre-defined date hierarchy.",
            )
            # condition = st.text_input(
            #     "Condition required to show this observation as a row, e.g. 'cmyn=1'"
            # )

        st.markdown("#")
        st.write("Optional fields")

        (
            col1,
            col2,
        ) = st.columns(2)

        with col1:
            st.write(
                "**is_present**: Records if the observation denotes presence (*true*)\
                      or absence (*false*) of the symptom."
            )
            subcol1, subcol2 = st.columns(2)
            is_present_field = subcol1.text_input("Field name", key="ispresent_field")
            is_present_values = subcol2.text_input("Value map", key="ispresent_value")
            st.write("Values: Records the value of **numerical observations**")
            value_field = st.text_input(
                "Field name",
                help="For numerical values - E.g., 'diabp_vsorres' storing the recorded\
                      blood pressure for the observation.",
                key="value_field",
            )
            subcol1, subcol2, subcol3 = st.columns(3)
            value_units = subcol1.text_input(
                "Desired unit for value (optional)",
                placeholder="kg",
                help="Desired unit for the value field, e.g. kg for mass, '°C' for\
                      temperature, years for age.",
                key="value_units_required",
            )
            value_sunit_field = subcol2.text_input(
                "Unit source field (optional)",
                help="Field name where the unit of the measurement taken is recorded",
                key="value_units_source",
            )
            value_sunits_map = subcol3.text_input(
                "Unit field mapping (optional)",
                placeholder="1=kg, 2=lbs",
                help="",
                key="value_units_map",
            )
            st.write("Text: records value map for **text-based observations**")
            subcol1, subcol2 = st.columns(2)
            text_field = subcol1.text_input("Field name", key="text_field")
            text_values = subcol2.text_input(
                "Value map",
                help="For text observations - E.g., for a conciousness scale,\
                     field = 'avpu_vsorres', values = '1=Alert, 2=Verbal, 3=Pain,\
                      4=Unresponsive' }.",
                key="text_value",
            )
        with col2:
            st.write(
                "**if**: Conditional controlling whether observation is included as a\
                      row in the output file."
            )
            condition = st.text_input("Condition, e.g. 'cmyn=1'")
            st.write("**Context**: Context that qualifies the observation")
            context = st.text_input(
                "Field name",
                help="e.g. *axillary* temperature, or *room air* oxygen saturation\
                      measurement",
            )
            st.write(
                "**Occurance period**: ISO 8601 duration string referring to the time\
                 period before the date in which observation occurred"
            )
            occurence_period = st.text_input("Field name")

            st.write("")
            st.write("")
            subcol1, subcol2, subcol3 = st.columns([1, 4, 1])
            add_observation = subcol2.form_submit_button(label=button_label)
        if add_observation:
            # check for potential dictionary entries
            try:
                is_present_values = string_to_dict(is_present_values)
            except ValueError:
                pass

            try:
                text_values = string_to_dict(text_values)
            except ValueError:
                pass

            if value_units != "":
                value = structures.field_with_unit(
                    value_field,
                    "",
                    value_units,
                    value_sunit_field,
                    string_to_dict(value_sunits_map),
                )
            else:
                value = value_field

            # write to a data store
            observation = {
                "name": name,
                "date": date,
                "phase": phase,
                "is_present": structures.field_value_mapped(
                    is_present_field, "", is_present_values
                ),
                "if": string_to_dict(condition, conditional=True),
                "value": value,
                "text": structures.field_value_mapped(text_field, "", text_values),
                "occurence_period": occurence_period,
                "context": context,
            }

            optional = ["is_present", "value", "text", "occurence_period", "context"]
            for f in optional:
                if observation[f] == "":
                    del observation[f]
                elif type(observation[f]) == dict:
                    if observation[f]["field"] == "":
                        del observation[f]

            return observation
