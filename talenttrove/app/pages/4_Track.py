import streamlit as st
import os
import sys
import requests

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
    url = "https://www.trustpilot.com/api/consumersitesearch-api/businessunits/search"
    params = {
        "country": "US",
        "page": 1,
        "pageSize": 1,
        "query": company_name,
    }
    try:
        response = requests.get(
            url, params=params, headers={"user-agent": "Mozilla/5.0"}
        )
        print(f"Trustpilot API Response: {response.status_code}")
        if pd.DataFrame(response.json().get("businessUnits", [])).shape[0] == 1:
            temp = pd.DataFrame(response.json().get("businessUnits", []))
            if pd.isna(temp["logoUrl"].iloc[0]):
                print("No Logo Found")
                return "https://storage.googleapis.com/simplify-imgs/company/default/logo.png"
            else:
                return f'https://consumersiteimages.trustpilot.net/business-units/{temp["businessUnitId"].iloc[0]}-198x149-1x.jpg'
    except Exception as e:
        print(e)
        pass
    return "https://storage.googleapis.com/simplify-imgs/company/default/logo.png"


openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")
gmail_username = st.session_state.get("GMAIL_USERNAME")

st.set_page_config(page_title="TalentTrove", page_icon="📖", layout="wide")
st.header("Application Tracker")

track_data = pd.read_csv(settings["Track_PATH"])


def get_last_update_date():
    return pd.read_csv(settings["Track_Date_PATH"])["Date"].max()


jobs = pd.DataFrame()
if st.button("Get Latest Track Data", type="primary"):
    if gmail_api_key and gmail_username:
        latest_date = get_last_update_date()
        if pd.isna(latest_date):
            # get date of one year ago from now and import libraries
            latest_date = (datetime.now() - timedelta(days=1)).strftime("%d-%b-%Y")
        with st.spinner(f"Fetching emails since {latest_date}..."):
            gmail = Gmail(username=gmail_username, password=gmail_api_key)
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
            jobs.to_csv("job_classification_test.csv", index=False)
            jobs["date"] = dates
            jobs = jobs[jobs["job"] != "0"]
            jobs.reset_index(inplace=True, drop=True)
            jobs["title"] = None
            jobs["company"] = None
            jobs["rejected"] = 0
            jobs[
                "logo"
            ] = "https://storage.googleapis.com/simplify-imgs/company/default/logo.png"  # deafult placeholder logo
            jobs["location"] = "Singapore"
            for index, i in enumerate(jobs["text"]):
                jobs.loc[index, "company"] = classifier.extractor.get_company(i)
                jobs.loc[index, "title"] = classifier.extractor.get_jobtitle(i)
                jobs.loc[index, "logo"] = get_logo_trustpilot(
                    jobs.loc[index, "company"]
                )
        if jobs.shape[0] == 0:
            st.warning("No new Job Update emails found")
        else:
            with st.spinner("Identifying Job Stage"):
                stage_classifier = JobStageClassifier()
                stages = []
                for index, i in enumerate(jobs["text"]):
                    out = stage_classifier.classify(i)
                    if int(out) == 4:  # rejected
                        jobs.loc[index, "rejected"] = 1
                    stages.append(int(out))
                jobs["stage"] = stages
                jobs[["text", "job", "stage", "company", "title"]].to_csv(
                    "job_stages_test.csv", index=False
                )
        print(jobs.head())
    else:
        st.error("Please enter your Gmail API Key or Gmail username")
        st.stop()
track_data = pd.concat([jobs, track_data], axis=0)
track_data.sort_values(by="date", inplace=True, ascending=True)
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

# storing the updated data
track_data.to_csv(settings["Track_PATH"], index=False)
