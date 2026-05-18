from typing import List
from .WebCrawler import WebCrawler
from Contracts.CrawledPage.CrawledPage import CrawledPage

def crawl_tourism_sites(seed_urls: List[str], max_pages: int = 50) -> List[CrawledPage]:
    """
    Crawls a list of seed URLs and their links up to a maximum number of pages.
    """
    crawler = WebCrawler(max_pages=max_pages)
    return crawler.crawl(seed_urls)
