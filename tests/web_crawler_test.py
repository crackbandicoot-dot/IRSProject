import pytest
from web_crawler.web_crawler import crawl_tourism_sites
from contracts.crawled_page.crawled_page import CrawledPage

def test_integration_crawl_tourism_sites() -> None:
    # We use a highly available URL related to tourism for the integration test.
    # Max entries is kept small to avoid long test run times blockings.
    seed_urls = ["https://en.wikipedia.org/wiki/Tourism"]
    max_pages = 2
    
    pages = crawl_tourism_sites(seed_urls, max_pages=max_pages)
    
    # Verify we got some pages crawled
    assert len(pages) > 0
    assert len(pages) <= max_pages, "Should not exceed max_pages"
    
    # Verify the structure of the returned objects
    first_page = pages[0]
    assert isinstance(first_page, CrawledPage)
    assert "wikipedia.org" in first_page.url
    assert isinstance(first_page.title, str)
    assert isinstance(first_page.content, str)
    assert len(first_page.title) > 0
    assert len(first_page.content) > 0

def test_integration_crawls_multiple_pages() -> None:
    # This test ensures the crawler is actually following links up to max_pages
    seed_urls = ["https://en.wikipedia.org/wiki/Tourism"]
    max_pages = 5
    
    pages = crawl_tourism_sites(seed_urls, max_pages=max_pages)
    
    # Verify it actually followed links and generated the max number of pages requested
    assert len(pages) == max_pages, f"Crawler should have found {max_pages} pages"
    
    url_set = {p.url for p in pages}
    assert len(url_set) == max_pages, "All crawled URLs should be unique"
    
    # At least one extracted page should be different from the seed URL
    assert any(p.url != seed_urls[0] for p in pages), "Crawler didn't traverse to any new URLs"

    # Verify that all pages have some valid content
    for page in pages:
        assert isinstance(page, CrawledPage)
        assert page.url.startswith("http")
        assert len(page.title) > 0, f"Page {page.url} is missing a title"
        assert len(page.content) > 0, f"Page {page.url} is missing content"
