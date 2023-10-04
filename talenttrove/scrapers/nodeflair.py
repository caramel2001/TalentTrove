import scrapy


class NodeFlairSpider(scrapy.Spider):
    name = "nodeflair"

    def __init__(self, category=None, *args, **kwargs):
        super(NodeFlairSpider, self).__init__(*args, **kwargs)
        self.start_urls = [f"https://nodeflair.com/api/v2/jobs?query=&page=1&sort_by=recent"]