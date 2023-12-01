import streamlit as st
import os
import logging
from streamlit_extras.tags import tagger_component
import pandas as pd

openai_api_key = st.session_state.get("OPENAI_API_KEY")
gmail_api_key = st.session_state.get("GMAIL_API_KEY")

logging.info("Jobs Rendered")

if not openai_api_key:
    st.warning(
        "Enter your OpenAI API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )
if not gmail_api_key:
    st.warning(
        "Enter your Gmail API key in the sidebar. You can get a key at"
        " https://platform.openai.com/account/api-keys."
    )
pwd = os.path.abspath(__file__)
directory = os.path.dirname(pwd)

data = pd.read_json(
    f"{directory}/../../data/jobs/mycareersfuture_cleaned.json",
    orient="records",
    lines=True,
)
data["updatedAt"] = pd.to_datetime(data["updatedAt"]).dt.date.astype(str)


# st.dataframe(data.head())
# Function to display a single job listing
def display_job(
    title,
    company,
    company_logo,
    apply_url,
    job_type=["Full-Time"],
    position_levels=["Entry Level"],
    date="",
):
    with st.container():
        col1, col2 = st.columns([1, 7])
        with col1:
            if company_logo is None:
                company_logo = f"{directory}/../static/logo.png"
            st.image(company_logo, width=50)  # Placeholder for company logo
        with col2:
            st.write(f"**{title}**")
            st.caption(f"{company}")
            st.markdown(f"**{date}**")
            tagger_component("", job_type[:3], color_name="lightblue")
            tagger_component("", position_levels[:3], color_name="blue")
            st.markdown("<br>", unsafe_allow_html=True)
            # st.button("Apply", key=title,type='primary')
            st.link_button("Apply", apply_url, type="primary")
            # col2.button("Apply", key=title,type='primary')


# Header of the page
st.title("Search for Jobs")

# Search bar
# search_query = st.text_input("Search for roles, companies, or locations")
css_body_container = """
    <style>
        [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"]
        [data-testid="stVerticalBlock"] {
            gap: 0;
        }
    </style>
    """
st.markdown(css_body_container, unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
# Filters
experience_level = col1.selectbox(
    "Experience Level", ["Fresh/entry level", "Executive", "Senior"]
)
category = col2.selectbox("Category", ["Technology", "Business", "Healthcare"])
job_type = col3.selectbox(
    "Job Type",
    ["Permanent", "Full Time", "Internship/Attachment", "Contract", "Freelance"],
)

data = data[data["employmentTypes"].apply(lambda x: job_type in x)]
data = data[data["positionLevels"].apply(lambda x: experience_level in x)]

# Display job listings
st.subheader("Results", divider="blue")
st.markdown("<br>", unsafe_allow_html=True)
num_results = len(data.head(20))
for i in range(0, num_results, 3):
    col1, col2, col3 = st.columns(3, gap="large")
    temp = data.iloc[i : i + 3]
    temp = temp[
        [
            "title",
            "company_name",
            "company_logo",
            "apply_url",
            "employmentTypes",
            "positionLevels",
            "updatedAt",
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
