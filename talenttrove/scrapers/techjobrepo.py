from talenttrove.scrapers.utils import HEADERS
import requests

import requests


class TechJobRepo:
    """
    A class for collecting tech job data from multiple URLs.

    Attributes:
        urls (list): A list of URLs to fetch job data from.
        verbose (bool): A flag indicating whether to print verbose output.

    Methods:
        collect(): Collects job data from the specified URLs and returns a list of jobs.
    """

    def __init__(self, verbose=True, *args, **kwargs):
        self.urls = [
            "https://job-finder-77bn.onrender.com/get/jobs/INTERN?posted=true",
            "https://job-finder-77bn.onrender.com/get/jobs/FRESH_GRAD?posted=true",
        ]
        self.verbose = verbose

    def collect(self):
        """
        Collects job data from the specified URLs.

        Returns:
            list: A list of job data extracted from the URLs.
        """
        jobs = []
        for url in self.urls:
            response = requests.get(url, headers=HEADERS)
            jobs.extend(response.json())
        if self.verbose:
            print(f"Extracted {len(jobs)} jobs")
        return jobs
