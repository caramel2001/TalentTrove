import os
import pandas as pd
import chromadb

documents = []
metadatas = []
ids = []

file_path = os.path.join(os.getcwd(),'talenttrove/data/jobs/mycareersfuture_with_descriptions_cleaned.json')
with open(file_path, 'r') as file:
    df = pd.read_json(file, orient='records')

for index, row in df.iterrows():
    company_name = row['company_name']
    uen = row['uen']
    job_post_id = row['jobPostId']

    documents.append(row['description'])
    metadatas.append({'company_name': company_name, 'uen': uen, 'job_post_id': job_post_id})
    ids.append(str(index))

chroma_client = chromadb.PersistentClient(path=os.path.join(os.getcwd(),"talenttrove/data/jd_vectordb"))
collection = chroma_client.get_or_create_collection(name="mycareersfuture_jd")
batch_size = 500  # Adjust this value based on the maximum batch size allowed
for i in range(0, len(documents), batch_size):
    batch_documents = documents[i:i+batch_size]
    batch_metadatas = metadatas[i:i+batch_size]
    batch_ids = ids[i:i+batch_size]

    # Ensure that the order of documents, metadatas, and ids is maintained within each batch
    assert len(batch_documents) == len(batch_metadatas) == len(batch_ids)

    # Add the batch to the collection
    collection.add(
        documents=batch_documents,
        metadatas=batch_metadatas,
        ids=batch_ids
    )