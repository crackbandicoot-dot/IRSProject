import pytest
import json
from unittest.mock import patch, MagicMock
from contracts.crawled_page.crawled_page import CrawledPage
from text_processor import text_processor
from contracts.errors import EmbeddingGenerationError

@pytest.fixture
def sample_page() -> CrawledPage:
    return CrawledPage(
        url="https://example.com/test",
        title="Hello World",
        content="This is a simple hello world test content. Hello test.",
        # Links attribute was removed or not present on CrawledPage contract
    )

def test_get_index_data_contains_document_and_postings(sample_page: CrawledPage) -> None:
    index_data = text_processor.get_index_data(sample_page)
    
    assert "document" in index_data
    assert "postings" in index_data
    
    doc = index_data["document"]
    assert doc["title"] == "Hello World"
    assert doc["content"] == "This is a simple hello world test content. Hello test."
    assert doc["url"] == "https://example.com/test"

def test_get_index_data_title_boosting(sample_page: CrawledPage) -> None:
    index_data = text_processor.get_index_data(sample_page)
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
    index_data = text_processor.get_index_data(empty_page)
    
    assert index_data["postings"] == []
    assert index_data["document"]["title"] == ""

@patch('urllib.request.urlopen')
def test_get_embedding_generates_correct_dimensions(mock_urlopen: MagicMock, sample_page: CrawledPage) -> None:
    # 'all-MiniLM-L6-v2' produces 384-dimensional embeddings
    mock_response = MagicMock()
    mock_response.read.return_value = json.dumps([[0.1] * 384]).encode('utf-8')
    mock_response.__enter__.return_value = mock_response
    mock_urlopen.return_value = mock_response

    embedding = text_processor.get_embedding(sample_page)
    
    assert isinstance(embedding, list)
    assert len(embedding) == 384
    assert isinstance(embedding[0], float)
    mock_urlopen.assert_called_once()

@patch('urllib.request.urlopen')
def test_get_embedding_handles_api_error(mock_urlopen: MagicMock, sample_page: CrawledPage) -> None:
    mock_urlopen.side_effect = Exception("API rate limited")

    with pytest.raises(EmbeddingGenerationError) as exc_info:
        text_processor.get_embedding(sample_page)
    
    assert "Embedding generation failed: API rate limited" in str(exc_info.value)
