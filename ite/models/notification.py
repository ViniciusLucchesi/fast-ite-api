import requests
from requests import Response
from dataclasses import dataclass, asdict
from selectolax.parser import HTMLParser, Node


@dataclass
class News:
    image: str
    date: str
    title: str
    link: str


@dataclass
class ScrapingRequest:
    status_code: int
    response: HTMLParser

    def __init__(self, url: str):
        data = self._get_html(url)
        self.status_code = data.status_code
        self.response = HTMLParser(data.text)

    def _get_html(self, url: str) -> Response:
        return requests.get(url)


@dataclass
class ScrapingNews:
    html: HTMLParser
    data: list[News] | list[dict]

    def __init__(self, url: str):
        data = ScrapingRequest(url)
        self.html = data.response
        self.list_nodes = self.get_all_cards()
        self.data = self.node_to_text()
    
    def __post_init__(self):
        self.data = self.class_to_dict()


    def get_all_cards(self) -> list[Node]:
        return self.html.css('div.card-n')

    def node_to_text(self) -> list[News]:
        news = []
        for item in self.list_nodes:
            image = item.css_first('img').attributes['src']
            date = item.css_first('span').text()
            title = item.css_first('p').text()
            link = item.css_first('a').attributes['href']
            news.append(News(image, date, title, link))
        return news

    def class_to_dict(self) -> list[dict]:
        return [asdict(item) for item in self.data]
