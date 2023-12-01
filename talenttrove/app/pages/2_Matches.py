import streamlit as st
import os
import logging
from recommendation.engine import Recommendation
openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")

logging.info('Matches Rendered')

if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )

uploaded_file = st.file_uploader(
    "Upload your Resumse (Supported pdf, docx)",
    type=["pdf", "docx"],
    help="Scanned documents are not supported yet!",
)

if not uploaded_file:
    st.warning(
        "Upload your Resumse (Supported pdf, docx) to get LLM recommended Matches"
    )
else:
    rec = Recommendation(uploaded_file,openai_api_key)
    print('Created Recommendation Object')
    with st.spinner('Generating Job Description...'):
        gen_jd = rec.get_generated_jd()
    similar_jds = rec.search_jd(gen_jd)
    st.write(similar_jds)