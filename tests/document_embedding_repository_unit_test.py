import typing
import pytest
from unittest.mock import MagicMock, patch
from DocumentEmbeddingRepository import document_embedding_repository
from Contracts.SearchResults.SearchResult import SearchResult

@pytest.fixture
def mock_repo() -> typing.Generator[MagicMock, None, None]:
    with patch('DocumentEmbeddingRepository.document_embedding_repository._repository') as mock:
        yield mock

def test_save(mock_repo: MagicMock) -> None:
    doc_id = "test_doc_1"
    embedding = [0.1, 0.2, 0.3, 0.4]
    document_embedding_repository.save(doc_id, embedding)
    mock_repo.save.assert_called_once_with(doc_id, embedding)

def test_delete(mock_repo: MagicMock) -> None:
    doc_id = "test_doc_1"
    document_embedding_repository.delete(doc_id)
    mock_repo.delete.assert_called_once_with(doc_id)

def test_get(mock_repo: MagicMock) -> None:
    doc_id = "test_doc_1"
    expected_embedding = [0.1, 0.2, 0.3, 0.4]
    mock_repo.get.return_value = expected_embedding
    result = document_embedding_repository.get(doc_id)
    mock_repo.get.assert_called_once_with(doc_id)
    assert result == expected_embedding

def test_get_not_found(mock_repo: MagicMock) -> None:
    doc_id = "non_existent_doc"
    mock_repo.get.return_value = None
    result = document_embedding_repository.get(doc_id)
    mock_repo.get.assert_called_once_with(doc_id)
    assert result is None

def test_semantic_search(mock_repo: MagicMock) -> None:
    query_embedding = [0.1, 0.2, 0.3, 0.4]
    limit = 5
    metric = "l2"
    expected_results = [MagicMock(spec=SearchResult)]
    mock_repo.semantic_search.return_value = expected_results
    results = document_embedding_repository.semantic_search(query_embedding, limit, metric)
    mock_repo.semantic_search.assert_called_once_with(query_embedding, limit, metric)
    assert results == expected_results

def test_semantic_search_default_args(mock_repo: MagicMock) -> None:
    query_embedding = [0.1, 0.2, 0.3, 0.4]
    expected_results = [MagicMock(spec=SearchResult)]
    mock_repo.semantic_search.return_value = expected_results
    results = document_embedding_repository.semantic_search(query_embedding)
    mock_repo.semantic_search.assert_called_once_with(query_embedding, 10, "cosine")
    assert results == expected_results
