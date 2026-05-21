from typing import List
from .web_crawler_impl import WebCrawler
from contracts.crawled_page.crawled_page import CrawledPage

def crawl(seed_urls: List[str], max_pages: int = 50) -> List[CrawledPage]:
    """
    Crawls a list of seed URLs and their links up to a maximum number of pages.
    """
    crawler = WebCrawler(max_pages=max_pages)
    return crawler.crawl(seed_urls)
