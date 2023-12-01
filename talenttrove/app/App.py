import streamlit as st
from components.sidebar import sidebar
from components.tracking import timeline
import os


EMBEDDING = "openi"
VECTOR_STORE = "faiss"
MODEL_LIST = ["gpt-3.5-turbo", "gpt-4"]

# Uncomment to enable debug mode
# MODEL_LIST.insert(0, "debug")

st.set_page_config(page_title="TalentTrove", page_icon="📖", layout="wide")
st.header("TalentTrove")

sidebar()

openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")


if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )
if not gmail_api_key:
    st.warning(
        "Enter your Gmail App Password in the sidebar. You can generate it at"
        " https://support.google.com/mail/answer/185833."
    )


st.image(os.path.join(os.getcwd(), "talenttrove/app/static/homepage.png"))
