import streamlit as st
import json
import forms.structures as structures

from forms.structures import string_to_dict, V_SPACE, recursive_search

parser = json.load(open("schemas/dev/parser.schema.json"))
obs = parser["properties"]["observation"]["items"]["properties"]["name"]["enum"]

# TODO: Add 'for' loop compatability
# TODO: Add option to take an existing field as an input


def cleanup_observation(aobservation, aobservation_type):
    """
    Removes any empty fields from a new observation record.
    """
    for f, label in zip(
        ["is_present", "value", "text"], ["presence/absence", "value", "text"]
    ):
        if aobservation_type == label:
            pass
        else:
            del aobservation[f]

    optional = [
        "if",
        "context",
        "start_date",
        "duration_type",
    ]
    for f in optional:
        if aobservation[f] == "":
            del aobservation[f]
        elif type(aobservation[f]) == dict:
            if "fields" in aobservation[f]:
                field = [
                    recursive_search(fld, "field") for fld in aobservation[f]["fields"]
                ]
                if all(fld == "" for fld in field):
                    del aobservation[f]
            else:
                field = recursive_search(aobservation[f], "field")

                if field == "" or not aobservation[f]:
                    del aobservation[f]

    return aobservation


def observation_form(button_label, clear_on_sub):
    with st.form(key="observation", clear_on_submit=clear_on_sub):
        st.write("Required fields:")
        (
            col1,
            col2,
        ) = st.columns(2)
        with col1:
            name = st.selectbox("Observation name", obs)
            phase = st.radio(
                "Observation phase", ["admission", "study", "followup"], horizontal=True
            )
        with col2:
            date = st.text_input(
                "Date of observation, or end-date if observed over a time period",
                value="admissionDateHierarchy",
                help="This can either be a single field name where the date is stored,\
                                or a reference to a pre-defined date hierarchy.",
            )

        V_SPACE(1)

        st.markdown("#### Optional fields")

        (
            col1,
            col2,
        ) = st.columns(2, gap="medium")

        with col1:
            observation_type = st.radio(
                "Type of observation:",
                ["presence/absence", "value", "text"],
                help="An observation can record one of three types of data: whether an\
                    observation is present or absent (e.g. loss of smell); a value\
                    (e.g. a heart rate in bmp); or a text observation (e.g. 'Verbal'\
                    as an AVPU response).)",
            )
            subcol1, subcol2 = st.columns(2)
            field = subcol1.text_input("Field name", key="ispresent_field")
            values = subcol2.text_input("Value map", key="field_value")
            subcol1, subcol2, subcol3 = st.columns(3)
            value_units = subcol1.text_input(
                "Desired unit for value",
                placeholder="kg",
                help="Optional: Desired unit for the value field, e.g. kg for mass,\
                      '°C' for temperature, years for age.",
                key="value_units_required",
            )
            value_sunit_field = subcol2.text_input(
                "Unit source field",
                help="Optional: Field name where the unit of the measurement taken is\
                      recorded",
                key="value_units_source",
            )
            value_sunits_map = subcol3.text_input(
                "Unit field mapping",
                placeholder="1=kg, 2=lbs",
                help="Optional: Value map for units, e.g. '1=years, 2=months'",
                key="value_units_map",
            )
            st.write("Condition to display the observation as an output")
            condition = st.text_input(
                "Condition",
                placeholder="cough_ceoccur!=3",
                help="An observation will only be shown in the long-format output table\
                 if this condition is met. E.g., for an observation field 'cough_cmyn'\
                 which indicates the presence/absence of a cough, where 1=yes, 0=no and\
                 3=unknown, a conditional statment of 'cough_cmyn!=3' is required\
                 so that the observation is not shown if no data was recorded.",
            )

        with col2:
            V_SPACE(2)
            st.write("**Context**: Context that qualifies the observation")
            subcol1, subcol2 = st.columns(2)
            context_single = subcol1.text_input(
                "Constant value",
                help="e.g., 'Highest', for a temperature reading over 24 hrs",
            )
            context_field = subcol2.text_input(
                "Field name",
                help="Use this instead of 'constant value' if a data field holds the\
                    context information.",
            )
            context_description = subcol1.text_input(
                "Context description", help="E.g., 'Oxygen saturation on:'"
            )
            context_values = subcol2.text_input(
                "Value map", help="E.g., 1=Room air, 2=Oxygen therapy"
            )

            start_date = st.text_input(
                "**Start date**: Start date of observation duration"
            )

            st.write("Required if a start date is provided:")
            duration_type = st.radio(
                "Duration type",
                ["event", "block"],
                help="The duration of an observation is an 'event' if it happens *once*\
                    , or a *number of discrete times*, over the time period. It is a\
                    'block' if the observation occured over *the entire observation\
                    period*.",
                horizontal=True,
            )

            st.write("")
            st.write("")
            subcol1, subcol2, subcol3 = st.columns([1, 4, 1])
            add_observation = subcol2.form_submit_button(label=button_label)
        if add_observation:
            # check for potential dictionary entries
            try:
                values = string_to_dict(values)
            except ValueError:
                pass

            try:
                context_values = string_to_dict(context_values)
            except ValueError:
                pass

            if value_units != "":
                value = structures.field_with_unit(
                    values,
                    "",
                    value_units,
                    value_sunit_field,
                    string_to_dict(value_sunits_map),
                )
            else:
                value = values

            # write to a data store
            observation = {
                "name": name,
                "date": date,
                "phase": phase,
                "is_present": structures.field_value_mapped(field, "", value),
                "if": string_to_dict(condition, conditional=True),
                "value": structures.field_value_mapped(field, "", value),
                "text": structures.field_value_mapped(field, "", value),
                "start_date": start_date,
                "duration_type": duration_type,
                "context": context_single
                if context_single != ""
                else structures.combined_type(
                    "set",
                    "",
                    [
                        {
                            "field": context_field,
                            "values": context_values,
                            "description": context_description,
                        }
                    ],
                ),
            }

            clean_observation = cleanup_observation(observation, observation_type)

            # for f, label in zip(
            #     ["is_present", "value", "text"], ["presence/absence", "value", "text"]
            # ):
            #     if observation_type == label:
            #         pass
            #     else:
            #         del observation[f]

            # optional = [
            #     "if",
            #     "context",
            #     "start_date",
            #     "duration_type",
            # ]
            # for f in optional:
            #     if observation[f] == "":
            #         del observation[f]
            #     elif type(observation[f]) == dict:
            #         if (
            #             "field" in observation[f] and observation[f]["field"] == ""
            #         ) or not observation[f]:
            #             del observation[f]

            return clean_observation
