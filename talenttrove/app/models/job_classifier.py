from talenttrove.app.email.gmail import Gmail
from datetime import datetime
from setfit import SetFitModel
from bs4 import BeautifulSoup
import os
import pandas as pd
from .flan import JobTitleCompanyNameExtractor
import gdown

email_classifier_model = "https://drive.google.com/drive/folders/1Jn_cjP1OjO5Ttj9-xs63o9cTPNhKwHOv?usp=drive_link"
file_path = os.path.dirname(os.path.abspath(__file__))
os.makedirs(file_path + "/model", exist_ok=True)
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
    return


class JobClassifier:
    def __init__(self) -> None:
        """
        Initializes the JobClassifier object.

        Downloads the model, loads the pretrained model, and initializes the JobTitleCompanyNameExtractor.
        """
        download_model()
        self.model = SetFitModel.from_pretrained(model_path)
        self.extractor = JobTitleCompanyNameExtractor()

    def infer(self, sentence):
        """
        Infers the class label for a given sentence.

        Args:
            sentence (str): The input sentence to classify.

        Returns:
            str: The predicted class label.
        """
        predtext = [sentence]
        predicted_class = self.model(predtext)
        return str(predicted_class.numpy()[0])

    def classify(self, email, preprocess=True):
        """
        Classifies an email into a specific category.

        Args:
            email (str): The email to classify.
            preprocess (bool, optional): Whether to preprocess the email before classification. Defaults to True.

        Returns:
            tuple: A tuple containing the preprocessed email and the predicted class label.
        """
        if preprocess:
            _, email = self.preprocess_email(email)

        predicted_class = self.infer(email)
        return _, predicted_class

    def preprocess_email(self, email):
        """
        Preprocesses an email by extracting the subject and cleaning the body.

        Args:
            email (str): The email to preprocess.

        Returns:
            tuple: A tuple containing the preprocessed email with subject and without subject.
        """
        try:
            subject = (email["subject"]).decode("utf-8")
        except:
            subject = email["subject"]
        html = str(BeautifulSoup(email["body"], "html.parser").text)
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
    specified_date = datetime(2023, 10, 1)
    formatted_date = specified_date.strftime("%d-%b-%Y")
    ids = gmail.get_email_by_date(from_date=formatted_date)
    # email_dict = gmail.parse_emails(ids[:5])
    preds = []
    df = pd.read_csv("emails_jobs.csv")
    print(df.head())
    for i in df["text"]:
        print(i[100:200])
        out = jc.classify(i, preprocess=False)
        print(out)
        preds.append(out)
    pd.Series(preds).to_csv("preds.csv")
