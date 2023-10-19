from talenttrove.scrapers.utils import HEADERS
import requests
TECH_COMPANIES = "https://nodeflair.com/blog/top-tech-companies-in-singapore"
class NodeFlairSpider():

    def __init__(self, category=None, *args, **kwargs):
        self.start_urls = [f"https://nodeflair.com/api/v2/jobs?query=&page=1&sort_by=recent"]

    def get_tech_companies(self,url=None):
        url = url or TECH_COMPANIES
        response = requests.get(url,headers=HEADERS)
