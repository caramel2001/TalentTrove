from talenttrove.scrapers.utils import HEADERS
import requests

class TechJobRepo:

    def __init__(self,verbose=True,*args, **kwargs):
        super(TechJobRepo, self).__init__(*args, **kwargs)
        self.urls = [f"https://job-finder-77bn.onrender.com/get/jobs/INTERN?posted=true","https://job-finder-77bn.onrender.com/get/jobs/FRESH_GRAD?posted=true"]
        self.verbose = True

    def collect(self):
        jobs=[]
        for url in self.urls:
            response = requests.get(url,headers=HEADERS)
            jobs.extend(response.json())
        if self.verbose:
            print(f"Extracted {len(jobs)} jobs")
        return jobs


