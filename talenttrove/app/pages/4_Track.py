import streamlit as st
import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    )
)
from models.job_classifier import JobClassifier
from models.job_stage import JobStageClassifier
from components.tracking import timeline, get_track_component
import pandas as pd
from config.config import settings
from datetime import datetime, timedelta
from talenttrove.app.email.gmail import Gmail


def get_logo_trustpilot(company_name):
    pass


def get_logo(company_name):
    pass


openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")

st.set_page_config(page_title="TalentTrove", page_icon="📖", layout="wide")
st.header("Application Tracker")

track_data = pd.read_csv(settings["Track_PATH"])


def get_last_update_date():
    return pd.read_csv(settings["Track_Date_PATH"])["Date"].max()


jobs = pd.DataFrame()
if st.button("Get Latest Track Data", type="primary"):
    if gmail_api_key:
        latest_date = get_last_update_date()
        if pd.isna(latest_date):
            # get date of one year ago from now and import libraries
            latest_date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        with st.spinner(f"Fetching emails since {latest_date}..."):
            gmail = Gmail(
                username="agarwalpratham2001@gmail.com", password=gmail_api_key
            )
            gmail.authenticate()
            ids = gmail.get_email_by_date(from_date=latest_date)
            email_dict = gmail.parse_emails(ids)
        with st.spinner("Identifying Job Emails"):
            classifier = JobClassifier()
            preds = []
            for i in email_dict:
                email, out = classifier.classify(i, preprocess=True)
                preds.append((email, out))
            dates = [pd.to_datetime(i["date"]).strftime("%d-%m-%Y") for i in email_dict]
        with st.spinner("Identifying Company and Job title"):
            jobs = pd.DataFrame(preds, columns=["text", "job"])
            jobs["date"] = dates
            jobs = jobs[jobs["job"] != "0"]
            jobs.reset_index(inplace=True, drop=True)
            jobs["title"] = None
            jobs["company"] = None
            jobs["rejected"] = False
            jobs[
                "logo"
            ] = "https://storage.googleapis.com/simplify-imgs/company/default/logo.png"  # deafulat placeholder logo
            jobs["location"] = None
            for index, i in enumerate(jobs["text"]):
                jobs.loc[index, "company"] = classifier.extractor.get_company(i)
                jobs.loc[index, "title"] = classifier.extractor.get_jobtitle(i)
        print(jobs.head())
        with st.spinner("Identifying Job Stage"):
            stage_classifier = JobStageClassifier()
            stages = []
            for i in jobs["text"]:
                out = stage_classifier.classify(i)
                stages.append(out)
            jobs["stage"] = stages
        print(jobs.head())
    else:
        st.error("Please enter your Gmail API Key")
        st.stop()
track_data = pd.concat([jobs, track_data], axis=0)
track_data.sort_values(by="date", inplace=True, ascending=False)
css_body_container = """
    <style>
        [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"]
        [data-testid="stVerticalBlock"] {
            gap: 0;
        }
    </style>
    """

st.markdown(css_body_container, unsafe_allow_html=True)
for i, row in track_data.iterrows():
    get_track_component(
        row["company"],
        row["title"],
        row["location"],
        row["logo"],
        row["stage"],
        row["date"],
        row["rejected"],
    )
