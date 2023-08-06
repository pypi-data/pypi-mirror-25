from urllib.request import urlopen

from bs4 import BeautifulSoup


class HTTPClient:
    tags = {}


    def __getattr__(self, item):
        return getattr(self.soup, item, None)


    def __init__(self, path: str):
        self.soup = self.load_url(path) if path.startswith('http') else self.load_file(path)


    def load_file(self, file_path):
        return BeautifulSoup(open(file_path), "html.parser","lxml")


    def load_url(self, url):
        html = urlopen(url)
        if html is None:
            return print("URL Not Found")
        return BeautifulSoup(html.read(),"lxml")
