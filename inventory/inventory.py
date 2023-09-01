from collections import defaultdict
from typing import Literal

import pandas as pd
import streamlit as st
import plotly.express as px


SHOW_LIMIT = 5  # do not display counts below this

SIDEBAR_TEXT = f"""## About

ISARIC Inventory shows aggregate statistics from a dataset collection curated by the
[ISARIC](https://isaric.org) consortium.

For privacy reasons, we only show the number of patients when there are >{SHOW_LIMIT} cases.
"""

st.set_page_config(
    page_title="ISARIC Inventory",
    layout="wide",
)
st.markdown(
    """<style>
textarea, html *  {
font-family: -apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif !important;
}
</style>""",
    unsafe_allow_html=True,
)

DATA = pd.read_csv("data.csv")
if "count" not in st.session_state:
    st.session_state.count = None


with st.sidebar:
    st.markdown(SIDEBAR_TEXT)

    st.radio("Gender", ["-", "male", "female"], horizontal=True, key="gender")
    st.multiselect(
        "Condition Present (any)", DATA.Condition.unique(), key="condition_present"
    )
    st.multiselect(
        "Condition Absent (any)", DATA.Condition.unique(), key="condition_absent"
    )

# display map

present = DATA[DATA.Condition.isin(st.session_state.condition_present) & DATA.IsPresent]
absent = DATA[DATA.Condition.isin(st.session_state.condition_absent) & ~DATA.IsPresent]
if present.empty and absent.empty:
    df = DATA[["PatientID", "Country_ISO3"]].drop_duplicates()
elif present.empty and not absent.empty:
    df = absent[["PatientID", "Country_ISO3"]].drop_duplicates()
elif absent.empty and not present.empty:
    df = present[["PatientID", "Country_ISO3"]].drop_duplicates()
else:
    common_patients = set(present.PatientID) & set(absent.PatientID)
    df = DATA[DATA.PatientID.isin(common_patients)][
        ["PatientID", "Country_ISO3"]
    ].drop_duplicates()

country_metrics = df.Country_ISO3.value_counts().reset_index()
country_metrics = country_metrics[country_metrics["count"] > SHOW_LIMIT]
st.metric("Patients", country_metrics["count"].sum())

fig = px.choropleth(country_metrics, locations="Country_ISO3", color="count")
st.plotly_chart(fig)
st.markdown("**Data**:")
st.dataframe(country_metrics)
