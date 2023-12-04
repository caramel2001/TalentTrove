from talenttrove.app.models.job_classifier import JobClassifier
from talenttrove.app.models.job_stage import JobStageClassifier
from talenttrove.app.models.flan import JobTitleCompanyNameExtractor
import pandas as pd
import streamlit as st
import requests


class Classifier:
    def __init__(self):
        self.job_classifier = JobClassifier()
        self.job_stage_classifier = JobStageClassifier()
        self.extractor = JobTitleCompanyNameExtractor()

    def classify_jobs(self, emails: list):
        preds = []
        for email in emails:
            email, out = self.job_classifier.classify(email)
            preds.append((email, out))
        return preds

    def get_company_title_logos(self, texts: list):
        title = []
        company = []
        logos = []
        for i in texts:
            company.append(self.extractor.get_company(i))
            title.append(self.extractor.get_jobtitle(i))
            logos.append(self.get_logo_trustpilot(company[-1]))
        return title, company, logos

    def classify_stage(self, texts: list):
        stages = []
        rejected = []
        for i in texts:
            out = self.job_stage_classifier.classify(i)
            if int(out) == 4:  # rejected
                rejected.append(1)
            else:
                rejected.append(0)
            stages.append(int(out))
        return stages, rejected

    @staticmethod
    def get_logo_trustpilot(company_name):
        url = (
            "https://www.trustpilot.com/api/consumersitesearch-api/businessunits/search"
        )
        params = {
            "country": "US",
            "page": 1,
            "pageSize": 1,
            "query": company_name,
        }
        try:
            response = requests.get(
                url, params=params, headers={"user-agent": "Mozilla/5.0"}
            )
            if pd.DataFrame(response.json().get("businessUnits", [])).shape[0] == 1:
                temp = pd.DataFrame(response.json().get("businessUnits", []))
                if pd.isna(temp["logoUrl"].iloc[0]):
                    print("No Logo Found")
                    return "https://storage.googleapis.com/simplify-imgs/company/default/logo.png"
                else:
                    return f'https://consumersiteimages.trustpilot.net/business-units/{temp["businessUnitId"].iloc[0]}-198x149-1x.jpg'
        except Exception as e:
            pass
        return "https://storage.googleapis.com/simplify-imgs/company/default/logo.png"

    def streamlit_classify(self, emails: list):
        with st.spinner("Identifying Job Emails"):
            preds = self.classify_jobs(emails)
        jobs = pd.DataFrame(preds, columns=["text", "job"])
        dates = [pd.to_datetime(i["date"]).strftime("%Y-%m-%d") for i in emails]
        jobs["date"] = dates
        jobs = jobs[jobs["job"] != "0"]
        with st.spinner("Extracting Company and Job Title"):
            titles, companies, logos = self.get_company_title_logos(
                jobs["text"].to_list()
            )
        jobs["title"] = titles
        jobs["company"] = companies
        jobs["logo"] = logos
        with st.spinner("Identifying Job Stage"):
            stages, rejected = self.classify_stage(jobs["text"].to_list())
        jobs["stage"] = stages
        jobs["rejected"] = rejected
        jobs["location"] = None  # TODO: Add location
        jobs.reset_index(inplace=True, drop=True)
        return jobs

    def group_updates(self,updates_df:pd.DataFrame):
        pass