import streamlit as st
import os
import logging
from config.config import settings
from recommendation.engine import Recommendation
import pandas as pd
from streamlit_extras.tags import tagger_component
import ast

openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")
gen_jd = st.session_state.get("GEN_JD", None)
logging.info("Matches Rendered")
if not os.path.exists(settings["VECTORDB_PATH"]):
    st.error(
        "Vector DB does not exist. Please run `poetry run python talenttrove/VectorDB/chroma.py` to create VectorDB"
    )
    st.stop()
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

df = None
gen_jd = None
if st.button(label="Not Happy with your matches😭? Regenerate Matches"):
    if uploaded_file:
        rec = Recommendation(uploaded_file, openai_api_key)
        print("Created Recommendation Object")
        with st.spinner("Regenerating Job Description..."):
            gen_jd = rec.get_generated_jd()
            st.session_state["GEN_JD"] = gen_jd
        with st.expander("LLM Generated Job Description"):
            st.write(gen_jd)
        similar_jds = rec.search_jd(gen_jd, k=20)
        df = pd.json_normalize(similar_jds["metadatas"][0])

if not uploaded_file:
    st.warning(
        "Upload your Resumse (Supported pdf, docx) to get LLM recommended Matches"
    )
elif gen_jd is None:
    rec = Recommendation(uploaded_file, openai_api_key)
    print("Created Recommendation Object")
    with st.spinner("LLM Generating Job Description..."):
        gen_jd = rec.get_generated_jd()
        st.session_state["GEN_JD"] = gen_jd
    with st.expander("LLM Generated Job Description"):
        st.write(gen_jd)
    similar_jds = rec.search_jd(gen_jd, k=20)
    df = pd.json_normalize(similar_jds["metadatas"][0])

pwd = os.path.abspath(__file__)
directory = os.path.dirname(pwd)


# st.dataframe(data.head())
# Function to display a single job listing
def display_job(
    title,
    company,
    company_logo,
    apply_url,
    job_type=["Full-Time"],
    date="",
):
    with st.container():
        col1, col2 = st.columns([1, 7])
        with col1:
            if pd.isna(company_logo) or company_logo == "":
                company_logo = f"{directory}/../static/logo.png"
            st.image(company_logo, width=50)  # Placeholder for company logo
        with col2:
            st.write(f"**{title}**")
            st.caption(f"{company}")
            st.markdown(f"**{date}**")
            tagger_component("", job_type[:3], color_name="lightblue")
            st.link_button("Apply", apply_url, type="primary")


if df is not None:
    df["jobtype"] = df["jobtype"].fillna("[]", inplace=True)
    df["jobtype"] = df.jobtype.apply(
        lambda x: ast.literal_eval(x) if not pd.isna(x) or x is not None else []
    )
    df["date"] = df["date"].apply(
        lambda x: pd.to_datetime(x).date().strftime("%d-%m-%Y")
    )
    df["apply_url"] = df["apply_url"].apply(
        lambda x: x
        if "/partner/jobListing.htm" not in x
        else f"https://www.glassdoor.sg{x}"
    )
    num_results = len(df)
    for i in range(0, num_results, 3):
        col1, col2, col3 = st.columns(3, gap="large")
        temp = df.iloc[i : i + 3]
        temp = temp[
            [
                "title",
                "company_name",
                "company_logo",
                "apply_url",
                "jobtype",
                "date",
            ]
        ].to_numpy()
        if not i >= num_results:
            with col1:
                # st.write(list(temp[0]))
                display_job(*list(temp[0]))
        if not i + 1 >= num_results:
            with col2:
                display_job(*list(temp[1]))
        if not i + 2 >= num_results:
            with col3:
                display_job(*list(temp[2]))
        st.markdown("<br><br>", unsafe_allow_html=True)
