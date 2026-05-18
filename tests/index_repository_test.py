import pytest
from typing import Generator
from IndexRepository.IndexRepository import IndexRepository


@pytest.fixture
def repo() -> Generator[IndexRepository, None, None]:
    repo = IndexRepository(db_name="irs_test_db")
    repo._postings.delete_many({}) # Clean up before test
    yield repo
    repo._postings.delete_many({}) # Clean up after test
    repo._client.close()

def test_create_and_read_index(repo: IndexRepository) -> None:
    repo.create_index("doc-1", {"apple": 0.8, "banana": 0.5})
    doc = repo.read_index("doc-1")
    
    assert doc is not None
    if doc is not None:
        assert doc.id == "doc-1"
        
        # Validate weights via private property or term extraction since we know it's a dict
        assert doc._term_weights.get("apple", 0.0) == pytest.approx(0.8)
        assert doc._term_weights.get("banana", 0.0) == pytest.approx(0.5)

def test_update_index(repo: IndexRepository) -> None:
    repo.create_index("doc-1", {"apple": 0.8})
    repo.update_index("doc-1", {"apple": 0.9, "cherry": 0.3})
    doc = repo.read_index("doc-1")
    
    assert doc is not None
    if doc is not None:
        assert doc._term_weights.get("apple", 0.0) == pytest.approx(0.9)
        assert doc._term_weights.get("cherry", 0.0) == pytest.approx(0.3)
        # Verify the old term is gone
        assert "banana" not in doc._term_weights

def test_delete_index(repo: IndexRepository) -> None:
    repo.create_index("doc-1", {"apple": 0.8})
    repo.delete_index("doc-1")
    doc = repo.read_index("doc-1")
    
    assert doc is None

def test_get_relevant_indexes(repo: IndexRepository) -> None:
    repo.create_index("doc-1", {"apple": 0.8, "banana": 0.5})
    repo.create_index("doc-2", {"apple": 0.4})
    repo.create_index("doc-3", {"cherry": 0.9})
    
    # Test finding term "apple"
    results = repo.get_relevant_indexes("apple AND banana")
    
    assert len(results) == 2
    doc_ids = [doc.id for doc in results]
    
    assert "doc-1" in doc_ids
    assert "doc-2" in doc_ids
    assert "doc-3" not in doc_ids
