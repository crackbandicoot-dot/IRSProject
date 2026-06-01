from typing import List
from .web_crawler_impl import WebCrawler
from contracts.crawled_page.crawled_page import CrawledPage
from contracts.either import railway
from shared.logger import get_logger

_logger = get_logger(__name__)

@railway
def crawl(seed_urls: List[str], max_pages: int = 50) -> List[CrawledPage]:
    """
    Crawls a list of seed URLs and their links up to a maximum number of pages.
    """
    _logger.info(f"Crawling with {len(seed_urls)} seed URLs up to {max_pages} pages")
    crawler = WebCrawler(max_pages=max_pages)
    return crawler.crawl(seed_urls)
