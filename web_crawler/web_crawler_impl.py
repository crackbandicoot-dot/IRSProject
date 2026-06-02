from typing import List, Set,Iterator
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser
from contracts.crawled_page.crawled_page import CrawledPage
from shared.logger import get_logger
import threading
from contracts.either import railway,Ok,Error
from collections import deque

logger = get_logger(__name__)
class WebCrawler:
    def __init__(self, max_pages: int = 50) -> None:
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()
        self.robots_parsers: dict[str, RobotFileParser] = {}
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'

    @railway
    def _is_allowed_by_robots(self, url: str) -> bool:
        parsed_url = urlparse(url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        if domain not in self.robots_parsers:
            rp = RobotFileParser()
            robots_url = urljoin(domain, "/robots.txt")
            rp.set_url(robots_url)
            response = requests.get(robots_url, headers={'User-Agent': self.user_agent}, timeout=5)
            if response.status_code == 200:
                    rp.parse(response.text.splitlines())
            self.robots_parsers[domain] = rp
            
        return self.robots_parsers[domain].can_fetch(self.user_agent, url)
    
    @railway
    def _process_page(self, url: str) -> tuple[CrawledPage | None, List[str]]:
            if not self._is_allowed_by_robots(url).unwrap():
                logger.info(f"Crawling URL {url} disallowed by robots.txt")
                self.visited_urls.add(url)

            # We add a generic User-Agent header as many sites (like wikipedia) block default python-requests headers.
            headers = {'User-Agent': self.user_agent}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                logger.warning(f"Skipping URL {url} due to status code {response.status_code} or non-HTML content")
                return None, []

            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = ""
            if soup.title and soup.title.string:
                title = soup.title.string
            content = soup.get_text(separator=' ', strip=True)
            
            page = CrawledPage(url=url, title=title, content=content)
            new_urls = self._extract_urls(soup, url)
            return page, new_urls    
    def _extract_urls(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        urls = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            parsed = urlparse(full_url)
            if parsed.scheme in ['http', 'https']:
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                urls.append(clean_url)
        return urls

    def crawl(self, seed_urls: List[str]) -> Iterator[CrawledPage]:
        pages_to_visit = deque(seed_urls)
        crawled_pages: List[CrawledPage] = []

        while pages_to_visit and len(self.visited_urls) < self.max_pages:
            url = pages_to_visit.popleft()
            logger.info(f"Crawling URL: {url}")
            if url in self.visited_urls:
                continue
            
            self.visited_urls.add(url)

            page_either =self._process_page(url)
          
            match page_either:
                case Ok((page, new_links)):
                    page, new_links = page, new_links
                case Error(err):
                    logger.warning(f"Failed to process page {url}: {err}")
                    self.visited_urls.add(url)
                    continue
            if page:
                yield page
                crawled_pages.append(page)
                
            for link in new_links:
                if link not in self.visited_urls:
                    pages_to_visit.append(link)
                
        return crawled_pages