import streamlit as st
import os
import pandas as pd
import numpy as np
openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")


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


col1, col2, col3 , col4= st.columns(4)
col1.metric("Numbers of Applications", "10", "+8%")
col2.metric("Wind", "9 mph", "-8%")
col3.metric("Humidity", "86%", "4%")
col4.metric("Humidity", "86%", "4%")
st.markdown("<br>",unsafe_allow_html=True)
st.subheader('Application Count', divider='blue')

# generate a time series sequence of 20 days
pd.date_range('2021-01-01', periods=20, freq='D')
chart_data = pd.DataFrame()
chart_data['date'] = pd.date_range('2023-11-01', periods=20, freq='D')
chart_data['application_count'] = np.random.randint(5, size=(20)).cumsum()
chart_data.set_index('date', inplace=True)
st.line_chart(chart_data)