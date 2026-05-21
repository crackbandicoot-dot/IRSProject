from dataclasses import dataclass

@dataclass
class CrawledPage:
    url: str
    title: str
    content: str
