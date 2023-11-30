from talenttrove.app.email.gmail import Gmail
from datetime import datetime
from setfit import SetFitModel
from bs4 import BeautifulSoup
import os
import pandas as pd
from flan import JobTitleCompanyNameExtractor
import gdown

# from huggingchat import HFJobTitleCompanyNameExtractor
from tqdm import tqdm

email_classifier_model = "https://drive.google.com/drive/folders/1IyNvT9vnCD91TgRFBiS4QKhS0Q0jQHJd?usp=drive_link"
file_path = os.path.dirname(os.path.abspath(__file__))
os.mkdir(file_path + "/model", exist_ok=True)
model_path = file_path + "/model/email_classifer"


def download_model():
    if os.path.exists(model_path):
        print("Model already exists")
        return
    print("Downloading model")

    gdown.download_folder(
        email_classifier_model,
        quiet=True,
        use_cookies=False,
        output=model_path,
    )


class JobClassifier:
    def __init__(self) -> None:
        download_model()
        self.model = SetFitModel.from_pretrained(model_path)
        self.extractor = JobTitleCompanyNameExtractor()

    def infer(self, sentence):
        predtext = [sentence]
        predicted_class = self.model(predtext)
        return str(predicted_class.numpy()[0])

    def classify(self, email):
        email, email_without_subject = self.preprocess_email(email)
        print(email_without_subject)
        predicted_class = self.infer(email_without_subject)
        return predicted_class

    def preprocess_email(self, email):
        try:
            subject = (email["subject"]).decode("utf-8")
        except:
            subject = email["subject"]
        html = str(BeautifulSoup(email["body"]).text)
        string_list = [s.strip() for s in str(html).split()]
        final_string = " ".join(string_list)
        final_string_without_subject = " ".join(string_list)
        final_string = "Subject: " + str(subject) + ". Body: " + final_string
        return final_string, final_string_without_subject


if __name__ == "__main__":
    jc = JobClassifier()
    gmail = Gmail(
        username="agarwalpratham2001@gmail.com", password="lgjc xmxv ixyr nvxx"
    )
    gmail.authenticate()
    specified_date = datetime(2023, 11, 30)
    formatted_date = specified_date.strftime("%d-%b-%Y")
    ids = gmail.get_email_by_date(from_date=formatted_date)
    email_dict = gmail.parse_emails(ids[:10])
    out = jc.classify(email_dict[0])
    print(out)
