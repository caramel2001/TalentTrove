from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch


class JobTitleCompanyNameExtractor:
    """
    A class for extracting job titles and company names from email text using the FLAN-T5 model.

    Args:
        model (str): The name or path of the FLAN-T5 model to use. Default is "google/flan-t5-base".

    Attributes:
        model (AutoModelForSeq2SeqLM): The FLAN-T5 model for sequence-to-sequence language modeling.
        tokenizer (AutoTokenizer): The tokenizer for the FLAN-T5 model.

    Methods:
        get_jobtitle(email_text: str) -> str: Extracts the job title from the given email text.
        get_company(email_text: str) -> str: Extracts the company name from the given email text.
    """

    def __init__(self, model="google/flan-t5-base"):
        """
        Initializes the JobTitleCompanyNameExtractor class.

        Args:
            model (str): The name or path of the FLAN-T5 model to use. Default is "google/flan-t5-base".
        """
        self.model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-base")
        self.tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-base")

    def get_jobtitle(self, email_text: str) -> str:
        """
        Extracts the job title from the given email text.

        Args:
            email_text (str): The text of the email.

        Returns:
            str: The extracted job title.
        """
        question = "What is the job title?"
        input_text = f"question: {question} context: {email_text}"
        inputs = self.tokenizer(
            input_text, return_tensors="pt", truncation=True, max_length=500
        )

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=20)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer

    def get_company(self, email_text: str) -> str:
        """
        Extracts the company name from the given email text.

        Args:
            email_text (str): The text of the email.

        Returns:
            str: The extracted company name.
        """
        question = "What is the name of the company?"
        input_text = f"question: {question} context: {email_text}"
        inputs = self.tokenizer(
            input_text, return_tensors="pt", truncation=True, max_length=500
        )

        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_new_tokens=20)
        answer = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return answer
