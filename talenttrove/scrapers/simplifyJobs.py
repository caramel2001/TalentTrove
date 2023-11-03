import json
import time  # Import the time module for sleep
import requests
from talenttrove.scrapers.utils import HEADERS

class SimplifyJobs:
    name = "simplifyjobs"
    start_url = "https://api.simplify.jobs/v2/company"

    def __init__(self, sleep_time=1, *args, **kwargs):
        self.sleep_time = int(sleep_time)
        self.verbose = True

    def requests_page(self,page):
        # Start with the first page
        response=requests.get(url=f"{self.start_url}?size=100&page={page}",headers=HEADERS)
        return response.json()
    
    def collect(self,page=1):
        self.datas = [   ]
        data = self.requests_page(page)
        self.datas.extend(data.get('items',[]))

        # Check if there are more pages to scrape
        total_pages = data.get('pages',0)
        while page < total_pages:
            page += 1
            if self.verbose:    
                print(f"Scraping next page: {page}")
            time.sleep(self.sleep_time)  # Sleep for the specified time (in seconds)
            # Continue to the next page
            data = self.requests_page(page)
            self.datas.extend(data.get('items',[]))
        return self.datas
            