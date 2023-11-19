import streamlit as st
import os
openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")




uploaded_file = st.file_uploader(
    "Upload your Resumse (Supported pdf, docx)",
    type=["pdf", "docx"],
    help="Scanned documents are not supported yet!",
)
if not uploaded_file:
    st.warning(
        "Upload your Resumse (Supported pdf, docx) to get LLM recommended Matches"
    )

if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )