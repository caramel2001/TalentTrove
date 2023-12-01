import streamlit as st
import os
import logging
import pandas as pd
import numpy as np
from config.config import settings

openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")


logging.info("Dashboard Rendered")

if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )
if not gmail_api_key:
    st.warning(
        "Enter your Gmail API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )

track_data = pd.read_csv(settings["Track_PATH"])
col1, col2, col3, col4 = st.columns(4)
col1.metric("Numbers of Applications", len(track_data))
col2.metric("Number of Interviews", len(track_data[track_data["stage"] == 2]))
col3.metric("Applications in Progress", len(track_data[track_data["rejected"] == 0]))
col4.metric("Number of Offers", len(track_data[track_data["stage"] == 3]))
st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Application Count")
st.markdown("<br>", unsafe_allow_html=True)
# generate a time series sequence of 20 days
chart_data = track_data
chart_data["date"] = pd.to_datetime(chart_data["date"], format="mixed")
chart_data = chart_data.resample("D", on="date").count().reset_index()
chart_data.set_index("date", inplace=True)
st.line_chart(chart_data["title"])

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Distribution of Applications by Stage")
st.markdown("<br>", unsafe_allow_html=True)
chart_data = track_data
chart_data = chart_data.value_counts(["stage"]).reset_index()
chart_data["stage"].replace(
    {0: "Applied", 1: "Assesment", 2: "Interview", 3: "Offer", 4: "Rejected"},
    inplace=True,
)
st.bar_chart(chart_data, x="stage", y="count", height=400, color="#189AB4")

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("Top 10 Companies by Number of Applications")
st.markdown("<br>", unsafe_allow_html=True)
chart_data = track_data
chart_data = (chart_data.value_counts(["company"]).reset_index()).head(10)
chart_data.sort_values("count", ascending=False, inplace=True)
st.bar_chart(chart_data, x="company", y="count", height=500, color="#ffaa00")
