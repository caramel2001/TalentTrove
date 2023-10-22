import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()


def sidebar():
    with st.sidebar:
        # st.markdown(
        #     "## How to use\n"
        #     "1. Enter your [OpenAI API key](https://platform.openai.com/account/api-keys) below🔑\n"  # noqa: E501
        #     "2. Upload a pdf, docx, or txt file📄\n"
        #     "3. Ask a question about the document💬\n"
        # )
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            placeholder="Paste your OpenAI API key here (sk-...)",
            help="You can get your API key from https://platform.openai.com/account/api-keys.",  # noqa: E501
            value=os.environ.get("OPENAI_API_KEY", None)
            or st.session_state.get("OPENAI_API_KEY", ""),
        )

        email_key_input = st.text_input(
            "Gmail App Password",
            type="password",
            placeholder="Paste your Gmail App Password here (sk-...)",
            help="You can get your API key from https://support.google.com/mail/answer/185833.",  # noqa: E501
            value=None
            or st.session_state.get("GMAIL_API_KEY", ""),
        )

        st.session_state["OPENAI_API_KEY"] = api_key_input
        st.session_state["GMAIL_API_KEY"] = email_key_input

        st.markdown("---")
        st.markdown("# About")
        st.markdown(
            "TalentTrove allows you track your job applications and manage your job search. "
            "The update is done by accessing your Email Inbox  "
        )
        

