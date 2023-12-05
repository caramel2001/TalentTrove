from talenttrove.scrapers.utils import HEADERS
import requests
import time
from tqdm import tqdm


import requests
import time
from tqdm import tqdm

class MyCareersFuture:
    """
    A class for scraping job data from MyCareersFuture website.
    """

    def __init__(self, verbose=True, *args, **kwargs):
        """
        Initialize the MyCareersFuture scraper.

        Args:
            verbose (bool, optional): Whether to print verbose output. Defaults to True.
        """
        self.url = f"https://api.mycareersfuture.gov.sg/v2/search"
        self.verbose = verbose

    def requests_page(self, page, json):
        """
        Send a POST request to retrieve job data for a specific page.

        Args:
            page (int): The page number to retrieve.
            json (dict): The JSON payload for the request.

        Returns:
            dict: The JSON response containing job data.
        """
        response = requests.post(
            url=f"{self.url}?limit=100&page={page}", headers=HEADERS, json=json
        )
        return response.json()

    def collect(self, sleep_time=1, json=None):
        """
        Collect job data from multiple pages.

        Args:
            sleep_time (int, optional): The time to sleep between requests. Defaults to 1.
            json (dict, optional): The JSON payload for the request. Defaults to None.

        Returns:
            list: A list of job data.
        """
        page = 1  # Start from page 1
        jobs = []
        json = json or {
            "employmentTypes": ["Full Time"],
            "positionLevels": ["Fresh/entry level"],
            "postingCompany": [],
        }
        data = self.requests_page(page, json=json)
        time.sleep(sleep_time)
        jobs.extend(data.get("results", []))
        total = data["total"] // 100
        print(f"Total pages {total}")
        for page in tqdm(range(2, total + 1)):
            data = self.requests_page(page, json=json)
            jobs.extend(data.get("results", []))
            time.sleep(sleep_time)
        if self.verbose:
            print(f"Extracted {len(jobs)} jobs")
        return jobs

    def get_job_data(self, id):
        """
        Get detailed job data for a specific job ID.

        Args:
            id (str): The ID of the job.

        Returns:
            dict: The JSON response containing detailed job data.
        """
        response = requests.get(
            f"https://api.mycareersfuture.gov.sg/v2/jobs/{id}?updateApplicationCount=true",
            headers=HEADERS,
        )
        return response.json()

    def clean_data():
        """
        Clean the job data.

        This method can be implemented to clean the job data collected.
        """
        pass
