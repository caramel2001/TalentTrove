import streamlit as st
import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from talenttrove.app.models.complete_classifier import Classifier
from talenttrove.app.components.tracking import get_track_component
import pandas as pd
import logging
from talenttrove.app.config.config import settings
from datetime import datetime, timedelta
from talenttrove.app.email.gmail import Gmail

openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")
gmail_username = st.session_state.get("GMAIL_USERNAME")

st.set_page_config(page_title="TalentTrove", page_icon="📖", layout="wide")
st.header("Application Tracker")

track_data = pd.read_csv(settings["Track_PATH"])

logging.info("Job Tracking Page Rendered")


def get_last_update_date():
    return pd.read_csv(settings["Track_Date_PATH"])["Date"].max()


jobs = pd.DataFrame()
latest_date = get_last_update_date()

if pd.isna(latest_date):
    # get date of one month ago from now
    latest_date = (datetime.now() - timedelta(days=2)).strftime("%d-%b-%Y")
    st.write("No previous update date found")
else:
    st.write(f"Last Updated on {latest_date}")

if st.button("Get Latest Track Data", type="primary"):
    if latest_date == datetime.now().strftime("%d-%b-%Y"):  # already updated today
        st.warning("No new Job Update emails found")
    else:
        if gmail_api_key and gmail_username:
            with st.spinner(f"Fetching emails since {latest_date}..."):
                gmail = Gmail(username=gmail_username, password=gmail_api_key)
                gmail.authenticate()
                ids = gmail.get_email_by_date(from_date=latest_date)
                email_dict = gmail.parse_emails(ids)
            # Classifier Pipeline
            with st.spinner("Intializing the models..."):
                classifier = Classifier()
            jobs = classifier.streamlit_classify(email_dict)
            print(jobs.head())
            # update last update date
            pd.DataFrame({"Date": [datetime.now().strftime("%d-%b-%Y")]}).to_csv(
                settings["Track_Date_PATH"], index=False
            )
        else:
            st.error("Please enter your Gmail API Key or Gmail username")

# updating the track data
track_data = pd.concat([jobs, track_data], axis=0)
track_data.sort_values(by="date", inplace=True, ascending=False)
# storing the updated data
track_data.to_csv(settings["Track_PATH"], index=False)

# group updates within same application
# Assumption : if a update has same company and title, it is the same application
grouped_track_data = (
    track_data.groupby(by=["company", "title"]).first().reset_index()
)  # TODO: Make it more robust
grouped_track_data.sort_values(by="date", inplace=True, ascending=False)

css_body_container = """
    <style>
        [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"]
        [data-testid="stVerticalBlock"] {
            gap: 0;
        }
    </style>
    """
# print(track_data.head())
# rendering the tracking components
st.markdown(css_body_container, unsafe_allow_html=True)
for i, row in grouped_track_data.iterrows():
    grouped_track_data, track_data = get_track_component(
        grouped_track_data, i, track_data
    )
