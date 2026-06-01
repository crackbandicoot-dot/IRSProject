import string
from typing import Any, Dict, List
from contracts.crawled_page.crawled_page import CrawledPage
from .text_processor_impl import TextProcessorImpl
from contracts.either import railway
from shared.logger import get_logger

_processor = TextProcessorImpl()
_logger = get_logger(__name__)

@railway
def get_index_data(page: CrawledPage) -> Dict[str, Any]:
    """
    Given a Crawled document, provides valid index data to update the DB.
    """
    _logger.info(f"Extracting index data for page: {page.url}")
    return _processor.get_index_data(page)

@railway
def get_embedding(text: str) -> List[float]:
    """
    Given a text string, returns an embedding representation useful for vector databases.
    """
    _logger.info(f"Generating embedding for text: {text[:min(30, len(text))]}...")  # Log only the first 30 characters for brevity
    return _processor.get_embedding(text)
