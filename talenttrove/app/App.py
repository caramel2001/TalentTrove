import streamlit as st
from components.sidebar import sidebar
from components.tracking import timeline
import os
import logging

EMBEDDING = "openi"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

logging.basicConfig(
    filename="app.log",
    encoding="utf-8",
    level=logging.INFO,
    format="%(asctime)s %(message)s",
)
logging.getLogger("PIL").setLevel(logging.WARNING)
# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="TalentTrove", page_icon="📖", layout="wide")
st.header("TalentTrove- All in One Job Application Tool")
st.write(
    """In the constantly changing world of work, finding a job has become a complicated and time-consuming process for those trying to progress in their careers. Acknowledging the difficulties that come with job hunting, we introduce TalentTrove—an all-in-one job recommendation and application tracking tool that simplifies the job application process and transforms the way job seekers navigate this journey.

The main problem for job seekers is the overwhelming and often disorganized process of applying for jobs. Without a central place to manage applications, and with an abundance of information, there is a risk of missing opportunities and facing potential setbacks in achieving career goals.

TalentTrove distinguishes itself by providing a central hub for job searching, easy-to-understand interfaces, and a simple way to track applications. Our focus on user-friendly navigation, along with advanced features like integrating job descriptions from platforms like Glassdoor and MyCareersFuture Singapore to recommend suitable job postings for the user, and utilizing Gmail API for efficient application progress tracking, positions TalentTrove as an innovative solution in tackling the challenges of the job application process.
"""
)
logging.info("TalentTrove Homepage Rendered")

sidebar()
openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")
gmail_username = st.session_state.get("GMAIL_USERNAME")


if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )
else:
    logging.info("OpenAI API key Entered")

if not gmail_api_key:
    st.warning(
        "Enter your Gmail App Password in the sidebar. You can generate it at"
        " https://support.google.com/mail/answer/185833."
    )
else:
    logging.info("Gmail key Entered")

if not gmail_username:
    st.warning("Enter your Gmail Email Address.")
else:
    logging.info("Gmail Email Entered")

st.image(os.path.join(os.getcwd(), "talenttrove/app/static/homepage.png"))
