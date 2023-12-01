import streamlit as st
import os
import sys
import pandas as pd
from config.config import settings

track_data = pd.read_csv(settings["Track_PATH"])
company = st.sidebar.selectbox("Company", track_data["company"].unique())
track_data = track_data[track_data["company"] == company]
jobtitle = st.sidebar.selectbox("Title", track_data["title"].unique())
track_data = track_data[track_data["title"] == jobtitle]
track_data["stage"].replace(
    {0: "Applied", 1: "Assesment", 2: "Interview", 3: "Offer", 4: "Rejected"},
    inplace=True,
)
if not company or not jobtitle:
    st.error("Please select a company and job title")
    st.stop()
for index, i in enumerate(track_data["text"]):
    with st.expander(
        f"{track_data.iloc[index]['date']} - {track_data.iloc[index]['stage']}"
    ):
        st.write(i)
