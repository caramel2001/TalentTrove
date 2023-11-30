
from hugchat import hugchat
from hugchat.login import Login
     
class HFJobTitleCompanyNameExtractor():
    def __init__(self,model='google/flan-t5-base'):

        self.password = 'ILoveDsai2024)'
        self.email = 'akshit.karanam99@gmail.com'
        sign = Login(self.email,self.password)
        self.cookies = sign.login()
        self.chatbot = hugchat.ChatBot(cookies=self.cookies.get_dict())


    def get_jobtitle(self,email_text:str):
        question =  "What is the job title or role?If not available output None. Only return the required field, do not generate other words or sentences.",
        input_text = f"question: {question} context: {email_text}"
        response = self.chatbot.chat(input_text)
        return response
    
    def get_company(self,email_text:str):
        question =  "What is the name of the company?If not available output None. Only return the required field, do not generate other words or sentences.",
        input_text = f"question: {question} context: {email_text}"
        response = self.chatbot.chat(input_text)
        return response
    