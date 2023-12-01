import os
import pandas as pd
import chromadb
from chromadb.utils import embedding_functions

documents = []
metadatas = []
ids = []

file_path = os.path.join(
    os.getcwd(), "talenttrove/data/jobs/mycareersfuture_with_descriptions_cleaned.json"
)
df = pd.read_json(file_path)

file_path = os.path.join(os.getcwd(), "talenttrove/data/jobs/ALL_Glass.csv")
df2 = pd.read_csv(file_path)

for index, row in df.iterrows():
    company_name = row["company_name"]
    if company_name == None:
        company_name = ""
    company_logo = row["company_logo"]
    if company_logo == None:
        company_logo = ""
    title = row["title"]
    if title == None:
        title = ""
    job_post_id = row["jobPostId"]
    if job_post_id == None:
        job_post_id = ""
    apply_url = row["apply_url"]
    if apply_url == None:
        apply_url = ""
    date = row["updatedAt"]
    if date == None:
        date = ""
    jobtype = str(row["positionLevels"])
    if jobtype == None:
        jobtype = ""

    documents.append(row["description"])
    metadatas.append(
        {
            "company_name": company_name,
            "company_logo": company_logo,
            "job_post_id": job_post_id,
            "title": title,
            "apply_url": apply_url,
            "date": date,
            "jobtype": jobtype,
        }
    )
    ids.append(str(index))

max_id = max(ids)
for index, row in df2.iterrows():
    company_name = row["employerNameFromSearch"]
    if company_name == None:
        company_name = ""
    company_logo = row["employer.squareLogoUrl"]
    if company_logo == None:
        company_logo = ""
    title = row["jobTitleText"]
    if title == None:
        title = ""
    job_post_id = row["jobReqId"]
    if job_post_id == None:
        job_post_id = ""
    apply_url = row["jobLink"]
    if apply_url == None:
        apply_url = ""
    date = row["discoverDate"]
    if date == None:
        date = ""
    jobtype = str(row["jobType"])
    if jobtype == None:
        jobtype = ""

    documents.append(row["cleaned_description"])
    metadatas.append(
        {
            "company_name": company_name,
            "company_logo": company_logo,
            "job_post_id": job_post_id,
            "title": title,
            "apply_url": apply_url,
            "date": date,
            "jobtype": jobtype,
        }
    )
    ids.append(str(max_id) + str(index))

chroma_client = chromadb.PersistentClient(
    path=os.path.join(os.getcwd(), "talenttrove/data/jd_vectordb")
)
collection = chroma_client.get_or_create_collection(
    name="mycareersfuture_jd",
    embedding_function=embedding_functions.DefaultEmbeddingFunction(),
)
batch_size = 500  # Adjust this value based on the maximum batch size allowed
for i in range(0, len(documents), batch_size):
    batch_documents = documents[i : i + batch_size]
    batch_metadatas = metadatas[i : i + batch_size]
    batch_ids = ids[i : i + batch_size]

    # Ensure that the order of documents, metadatas, and ids is maintained within each batch
    assert len(batch_documents) == len(batch_metadatas) == len(batch_ids)

    # Add the batch to the collection

    collection.add(documents=batch_documents, metadatas=batch_metadatas, ids=batch_ids)
