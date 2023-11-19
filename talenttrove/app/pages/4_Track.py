import streamlit as st
import os
from components.tracking import timeline,get_track_component
import pandas as pd
openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")

st.set_page_config(page_title="TalentTrove", page_icon="📖", layout="wide")
st.subheader("Application Tracker")


css_body_container = '''
    <style>
        [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"]
        [data-testid="stVerticalBlock"] {
            gap: 0;
        }
    </style>
    '''
dummy_data = pd.read_csv("talenttrove/data/dummy_data/applications.csv")
st.markdown(css_body_container,unsafe_allow_html=True)
for i,row in dummy_data.iterrows():
    get_track_component(row['company'],row['title'],row['location'],row['logo'],row['stage'],row['date'],row['rejected'])
