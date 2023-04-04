# observations.py

import streamlit as st
import pandas as pd

from forms.structures import sidebar_search

from webapp import generate_parser
from forms.observation import observation_form

if "obs_list" not in st.session_state:
    st.session_state.obs_list = []

with st.sidebar:
    sidebar_search("observations")

df = pd.DataFrame(st.session_state.obs_list)

st.header("Observations table")
st.write(
    "All the available mapping fields (based on the ISARIC schema) for the observations\
     table are listed below. Constant fields will be taken automatically from the\
          study-level table on the home page."
)
st.write(
    "For every observation in your form, fill in this form. When the 'add this\
     observation to the data store' button is clicked, it will be added to memory.\
     The currently stored observations are listed under the form. Observations which\
     are already present can be overwritten by filling in the form with the same\
     observation name and phase."
)

st.markdown("#")
# I think theres an issue with the way this is done, because i think you can have
# observations which have the same name and phase. - e.g. from different follow-up
# forms.

observation = observation_form("Add this observation field to data store", True)

if observation is not None:
    # here, search for whether the key has been written before, and overwrite if it has.
    overwrite = False
    # filter(lambda obs: obs['name'] == 'anorexia' and obs['phase'] == 'study', st.session_state.toml_dict['observation'])
    # search on the fieldname instead - that should always be different? that's the whole point after all
    for i, d in enumerate(st.session_state.obs_list):
        if d["name"] == observation["name"] and d["phase"] == observation["phase"]:
            st.session_state.obs_list[i] = observation
            overwrite = True
            break

    if overwrite is False:
        st.session_state.obs_list.append(observation)

    # df = pd.json_normalize(st.session_state.obs_list, max_level=0)
    df = pd.DataFrame(st.session_state.obs_list)


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

st.markdown("### Observations currently stored in memory")
st.table(df)
