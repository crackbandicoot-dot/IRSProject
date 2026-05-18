from typing import List, Set
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from Contracts.CrawledPage.CrawledPage import CrawledPage

class WebCrawler:
    def __init__(self, max_pages: int = 50) -> None:
        self.max_pages = max_pages
        self.visited_urls: Set[str] = set()

    def _process_page(self, url: str) -> tuple[CrawledPage | None, List[str]]:
        try:
            # We add a generic User-Agent header as many sites (like wikipedia) block default python-requests headers.
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code != 200 or 'text/html' not in response.headers.get('Content-Type', ''):
                return None, []

            soup = BeautifulSoup(response.text, 'html.parser')
            title = soup.title.string if soup.title else ""
            content = soup.get_text(separator=' ', strip=True)
            
            page = CrawledPage(url=url, title=title, content=content)
            new_urls = self._extract_urls(soup, url)
            return page, new_urls
            
        except Exception:
            return None, []
            
    def _extract_urls(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        urls = []
        for link in soup.find_all('a', href=True):
            full_url = urljoin(base_url, link['href'])
            parsed = urlparse(full_url)
            if parsed.scheme in ['http', 'https']:
                clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
                urls.append(clean_url)
        return urls

    def crawl(self, seed_urls: List[str]) -> List[CrawledPage]:
        pages_to_visit = seed_urls.copy()
        crawled_pages: List[CrawledPage] = []

        while pages_to_visit and len(self.visited_urls) < self.max_pages:
            url = pages_to_visit.pop(0)

            if url in self.visited_urls:
                continue
                
            self.visited_urls.add(url)
            page, new_links = self._process_page(url)
            
            if page:
                crawled_pages.append(page)
                
            for link in new_links:
                if link not in self.visited_urls and link not in pages_to_visit:
                    pages_to_visit.append(link)
                
        return crawled_pages
