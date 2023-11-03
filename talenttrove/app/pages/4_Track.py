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
dummy_data = pd.read_csv("/Users/pratham/Desktop/trademaster/TalentTrove/talenttrove/data/dummy_data/applications.csv")
st.markdown(css_body_container,unsafe_allow_html=True)
for i,row in dummy_data.iterrows():
    get_track_component(row['company'],row['title'],row['location'],row['logo'],1)
# col1,col2 = st.columns([1,2])
# with col2:
#     timeline(1)
# with col1:
#     # Title
   
#     # Logo, Company Name, and Location in a single column
#     col1, col2 = st.columns([1, 2.5])

#     with col1:
#         st.image("https://storage.googleapis.com/simplify-imgs/companies/d3613d51-4f2f-43c1-8952-1f91bf5a8bf8/logo.png", use_column_width=True)  # Replace "vatic_logo.png" with the path to your logo image

#     with col2:
#         st.markdown("**Algorithmic Trader**")
#         st.write("Vatic Investments")
#         st.caption("📍 New York, NY, USA")