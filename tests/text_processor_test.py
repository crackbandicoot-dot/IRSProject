import pytest
import json
from unittest.mock import patch, MagicMock
from contracts.crawled_page.crawled_page import CrawledPage
from text_processor import text_processor
from contracts.errors import EmbeddingGenerationError
from contracts.either import Error
import numpy as np
@pytest.fixture
def sample_page() -> CrawledPage:
    return CrawledPage(
        url="https://example.com/test",
        title="Hello World",
        content="This is a simple hello world test content. Hello test.",
        # Links attribute was removed or not present on CrawledPage contract
    )

def test_get_index_data_contains_document_and_postings(sample_page: CrawledPage) -> None:
    index_data_either = text_processor.get_index_data(sample_page)
    assert not isinstance(index_data_either,Error)
    index_data = index_data_either.unwrap()
    assert "document" in index_data
    assert "postings" in index_data
    
    doc = index_data["document"]
    assert doc["title"] == "Hello World"
    assert doc["content"] == "This is a simple hello world test content. Hello test."
    assert doc["url"] == "https://example.com/test"

def test_get_index_data_title_boosting(sample_page: CrawledPage) -> None:

    index_data_either = text_processor.get_index_data(sample_page)
    assert not isinstance(index_data_either,Error)
    index_data = index_data_either.unwrap()
    postings = {p["term"]: p["weight"] for p in index_data["postings"]}
    
    # 'hello' appears twice in content (2) and once in title (boosted +2) -> total 4
    # 'world' appears once in content (1) and once in title (boosted +2) -> total 3
    # 'test' appears twice in content (2) -> total 2
    # 'this' appears once in content (1) -> total 1
    
    assert "hello" in postings
    assert "world" in postings
    assert "test" in postings
    
    assert postings["hello"] > postings["test"]
    assert postings["world"] > postings["test"]

def test_get_index_data_empty_content() -> None:
    empty_page = CrawledPage(url="https://example.com", title="", content="")
    index_data_either = text_processor.get_index_data(empty_page)
    assert not isinstance(index_data_either,Error)
    index_data = index_data_either.unwrap()
    assert index_data["postings"] == []
    assert index_data["document"]["title"] == ""


def test_get_embedding_generates_correct_dimensions(sample_page: CrawledPage) -> None:
    
    embedding_either = text_processor.get_embedding(sample_page)
    assert not isinstance(embedding_either,Error)
    embedding = embedding_either.unwrap()
    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert isinstance(embedding[0], float)

def test_get_embedding_consistency(sample_page: CrawledPage) -> None:
    
    for _ in range(0,1000):
        embedding_either = text_processor.get_embedding(sample_page)
        assert not isinstance(embedding_either,Error)
        embedding = embedding_either.unwrap()
        assert isinstance(embedding, list)
        assert len(embedding) == 384
        assert isinstance(embedding[0], float)