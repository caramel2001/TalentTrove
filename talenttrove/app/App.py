import streamlit as st
from components.sidebar import sidebar
from components.tracking import timeline


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

st.markdown("<br>", unsafe_allow_html=True )
css_body_container = '''
    <style>
        [data-testid="stSidebar"] + section [data-testid="stVerticalBlock"]
        [data-testid="stVerticalBlock"] {
            gap: 0;
        }
    </style>
    '''
st.markdown(css_body_container,unsafe_allow_html=True)
col1,col2 = st.columns([1,2])
with col2:
    timeline(1)
with col1:
    # Title
   
    # Logo, Company Name, and Location in a single column
    col1, col2 = st.columns([1, 2.5])

    with col1:
        st.image("https://storage.googleapis.com/simplify-imgs/companies/d3613d51-4f2f-43c1-8952-1f91bf5a8bf8/logo.png", use_column_width=True)  # Replace "vatic_logo.png" with the path to your logo image

    with col2:
        st.markdown("**Algorithmic Trader**")
        st.write("Vatic Investments")
        st.caption("📍 New York, NY, USA")
# st.markdown("---",unsafe_allow_html=True)
# uploaded_file = st.file_uploader(
#     "Upload a pdf, docx, or txt file",
#     type=["pdf", "docx", "txt"],
#     help="Scanned documents are not supported yet!",
# )

# model: str = st.selectbox("Model", options=MODEL_LIST)  # type: ignore

# with st.expander("Advanced Options"):
#     return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
#     show_full_doc = st.checkbox("Show parsed contents of the document")


# if not uploaded_file:
#     st.stop()

# try:
#     file = read_file(uploaded_file)
# except Exception as e:
#     display_file_read_error(e, file_name=uploaded_file.name)

# chunked_file = chunk_file(file, chunk_size=300, chunk_overlap=0)

# if not is_file_valid(file):
#     st.stop()


# if not is_open_ai_key_valid(openai_api_key, model):
#     st.stop()


# with st.spinner("Indexing document... This may take a while⏳"):
#     folder_index = embed_files(
#         files=[chunked_file],
#         embedding=EMBEDDING if model != "debug" else "debug",
#         vector_store=VECTOR_STORE if model != "debug" else "debug",
#         openai_api_key=openai_api_key,
#     )

# with st.form(key="qa_form"):
#     query = st.text_area("Ask a question about the document")
#     submit = st.form_submit_button("Submit")


# if show_full_doc:
#     with st.expander("Document"):
#         # Hack to get around st.markdown rendering LaTeX
#         st.markdown(f"<p>{wrap_doc_in_html(file.docs)}</p>", unsafe_allow_html=True)


# if submit:
#     if not is_query_valid(query):
#         st.stop()

#     # Output Columns
#     answer_col, sources_col = st.columns(2)

#     llm = get_llm(model=model, openai_api_key=openai_api_key, temperature=0)
#     result = query_folder(
#         folder_index=folder_index,
#         query=query,
#         return_all=return_all_chunks,
#         llm=llm,
#     )

#     with answer_col:
#         st.markdown("#### Answer")
#         st.markdown(result.answer)

#     with sources_col:
#         st.markdown("#### Sources")
#         for source in result.sources:
#             st.markdown(source.page_content)
#             st.markdown(source.metadata["source"])
#             st.markdown("---")