from sentence_transformers import SentenceTransformer

# Job recommendation engine and UI to display them
class Recommendation:
    def __init__(self,resume,openai_key=None,jobtitle=None,model = 'all-MiniLM-L6-v2'):
        self.resume = resume
        self.jobtitle = jobtitle
        self.openai_key = openai_key
        self.model = SentenceTransformer(model)

    def get_generated_jd(self):
        # Get the generated JD from OpenAI API
        pass

    def search_jd(self,jd):
        embed = self.encode(jd)
        # Query most similar JDs from the vector database
        pass

    def encode(self,text:str):
        # Encode the JD before Searching
        return self.model.encode(text)
        

    def get_recommendations(self):
        pass
