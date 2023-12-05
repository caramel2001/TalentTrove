import os
from docx import Document
from openai import OpenAI
import chromadb
import logging
from chromadb.utils import embedding_functions


# Job recommendation engine and UI to display them
import os
import logging
from docx import Document
from openai import OpenAI
import chromadb
from chromadb import embedding_functions


class Recommendation:
    """
    Class for generating job recommendations based on a given resume.
    """

    def __init__(self, resume, openai_key=None, jobtitle=None):
        """
        Initializes a Recommendation object.

        Args:
            resume (str): The path or I/O object of the resume.
            openai_key (str, optional): The OpenAI API key. Defaults to None.
            jobtitle (str, optional): The job title. Defaults to None.
        """
        self.resume = resume
        self.jobtitle = jobtitle
        self.openai_key = openai_key
        self.client = OpenAI(api_key=self.openai_key)
        self.file_path = os.path.join(os.getcwd(), "talenttrove/data/jd_vectordb")
        self.chroma_client = chromadb.PersistentClient(path=self.file_path)
        self.collection = self.chroma_client.get_or_create_collection(
            name="mycareersfuture_jd",
            embedding_function=embedding_functions.DefaultEmbeddingFunction(),
        )

    def read_word_document(self):
        """
        Reads the word document and returns its content as text.

        Returns:
            str: The content of the word document.
        """
        doc = Document(self.resume)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text

    def get_generated_jd(self):
        """
        Generates a job description based on the given resume.

        Returns:
            str: The generated job description.
        """
        text = self.read_word_document()
        logging.info("Document Read")
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Based on the given resume above, create a suitable job posting for this resume. The job posting must include the job description, job responsibilities, and requirements such as qualifications and skills. Do not include the company name and location in this job posting.",
                    },
                    {
                        "role": "user",
                        "content": f"Resume: {text}\n\n---\n\nJob Description:",
                    },
                ],
                temperature=0.3,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            logging.info("CV Generated")
            return response.choices[0].message.content.strip()
        except Exception as e:
            logging.warning(e)
            print(e)
            return ""

    def search_jd(self, jd, k=10):
        """
        Searches for job descriptions similar to the given job description.

        Args:
            jd (str): The job description to search for.
            k (int, optional): The number of results to return. Defaults to 10.

        Returns:
            dict: The search results containing documents, distances, and metadatas.
        """
        results = self.collection.query(
            query_texts=[jd],
            n_results=k,
            include=["documents", "distances", "metadatas"],
        )
        return results
