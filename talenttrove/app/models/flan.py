from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch


class JobTitleCompanyNameExtractor:
    def __init__(self, model="google/flan-t5-base"):
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

    def get_jobtitle(self, email_text: str):
        question = "What is the job title?"
        input_text = f"question: {question} context: {email_text}"
        inputs = self.tokenizer(
            input_text, return_tensors="pt", truncation=True, max_length=500
        )

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=20)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer

    def get_company(self, email_text: str):
        question = "What is the name of the company?"
        input_text = f"question: {question} context: {email_text}"
        inputs = self.tokenizer(
            input_text, return_tensors="pt", truncation=True, max_length=500
        )

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=20)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
