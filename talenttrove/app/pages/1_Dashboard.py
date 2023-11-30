import streamlit as st
import os
import pandas as pd
import numpy as np
import plotly.express as px

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
col2.metric("Applications in Progress", "3", "+28%")
col3.metric("Applications Rejected", "2", "-16%")
col4.metric("Application Accepted", "5", "+30%")
st.markdown("<br>",unsafe_allow_html=True)
st.subheader('Application Count', divider='blue')

# generate a time series sequence of 20 days
pd.date_range('2021-01-01', periods=20, freq='D')
chart_data = pd.DataFrame()
chart_data['date'] = pd.date_range('2023-11-01', periods=20, freq='D')
chart_data['application_count'] = np.random.randint(5, size=(20)).cumsum()
chart_data.set_index('date', inplace=True)
st.line_chart(chart_data)

# scatter plot for status changes
np.random.seed(42)

size_group1 = 5
size_group2 = 8
size_group3 = 7

date_range = pd.date_range('2021-01-01', periods=20, freq='D')

values_group1 = np.random.rand(size_group1)
values_group2 = np.random.rand(size_group2)
values_group3 = np.random.rand(size_group3)

data = {
    'Date': np.repeat(date_range, 1),
    'Value': np.concatenate([values_group1, values_group2, values_group3]),
    'Status': np.concatenate([['Applied'] * size_group1, ['Rejected'] * size_group2, ['Accepted'] * size_group3])
}
df = pd.DataFrame(data)

fig = px.scatter(df, x='Date', y='Value', color='Status', title='Application Progress')

st.plotly_chart(fig)

# bar chart for categories of jobs applied
job_categories = [
    'Accounting / Auditing / Taxation',
    'Admin / Secretarial',
    'Advertising / Media',
    'Architecture / Interior Design',
    'Banking and Finance',
    'Building and Construction',
    'Consulting',
    'Customer Service',
    'Design',
    'Education and Training',
    'Engineering',
    'Entertainment',
    'Environment / Health',
    'Events / Promotions',
    'F&B',
    'General Management',
    'General Work',
    'Healthcare / Pharmaceutical',
    'Hospitality',
    'Human Resources',
    'Information Technology',
    'Insurance',
    'Legal',
    'Logistics / Supply Chain',
    'Manufacturing',
    'Marketing / Public Relations',
    'Medical / Therapy Services',
    'Others',
    'Personal Care / Beauty',
    'Precision Engineering',
    'Professional Services',
    'Public / Civil Service',
    'Purchasing / Merchandising',
    'Real Estate / Property Management',
    'Repair and Maintenance',
    'Risk Management',
    'Sales / Retail',
    'Sciences / Laboratory / R&D',
    'Security and Investigation',
    'Social Services',
    'Telecommunications',
    'Travel / Tourism',
    'Wholesale Trade'
]

job_applications = pd.DataFrame({
    'Category': job_categories,
    'Count': np.random.randint(1, 50, len(job_categories))
})

fig = px.bar(job_applications, x='Category', y='Count', title='Job Applications by Category')

fig.update_layout(
    xaxis_title='Job Category',
    yaxis_title='Count',
    xaxis_tickangle=-45,
    bargap=0.2
)

st.plotly_chart(fig)