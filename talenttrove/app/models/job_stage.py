from talenttrove.app.email.gmail import Gmail
from datetime import datetime
from setfit import SetFitModel
import os
import pandas as pd
import gdown

stage_classifier_model = "https://drive.google.com/drive/folders/1gq-9kA_MIa6KsULSjWC9lHyQXXgWFekT?usp=drive_link"
file_path = os.path.dirname(os.path.abspath(__file__))
os.makedirs(file_path + "/model", exist_ok=True)
model_path = file_path + "/model/stage_classifer"


def download_model():
    if os.path.exists(model_path):
        print("Model already exists")
        return
    print("Downloading model")

    gdown.download_folder(
        stage_classifier_model,
        quiet=True,
        use_cookies=False,
        output=model_path,
    )
    return


class JobStageClassifier:
    def __init__(self) -> None:
        """
        Initializes the JobStageClassifier class.
        Downloads the model and loads it for inference.
        """
        download_model()
        self.model = SetFitModel.from_pretrained(model_path)

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

    def classify(self, email):
        """
        Classifies an email into a specific job stage.

        Args:
            email (str): The email content to classify.

        Returns:
            str: The predicted job stage class label.
        """
        predicted_class = self.infer(email)
        return predicted_class
