from typing import Any, Dict, List
from contracts.crawled_page.crawled_page import CrawledPage
from .text_processor_impl import TextProcessorImpl

_processor = TextProcessorImpl()

def get_index_data(page: CrawledPage) -> Dict[str, Any]:
    """
    Given a Crawled document, provides valid index data to update the DB.
    """
    return _processor.get_index_data(page)

def get_embedding(page: CrawledPage) -> List[float]:
    """
    Given a Crawled document, returns an embedding representation useful for vector databases.
    """
    return _processor.get_embedding(page)
