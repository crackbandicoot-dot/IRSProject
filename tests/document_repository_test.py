import pytest
from typing import Generator
from DocumentRepository.DocumentRepository import DocumentRepository

@pytest.fixture
def repo() -> Generator[DocumentRepository, None, None]:
    repo = DocumentRepository(db_name="irs_test_db")
    repo._documents.delete_many({}) # Clean up before test
    yield repo
    repo._documents.delete_many({}) # Clean up after test
    repo._client.close()

def test_create_and_read_document(repo: DocumentRepository) -> None:
    repo.create_document("doc-1", {"title": "Test Document", "content": "Hello World"})
    doc = repo.read_document("doc-1") 
    assert doc is not None, "Expected to find document with id 'doc-1'"
    assert doc["title"] == "Test Document"
    assert doc["content"] == "Hello World"
    assert doc["id"] == "doc-1"
    assert "_id" not in doc

def test_update_document(repo: DocumentRepository) -> None:
    repo.create_document("doc-1", {"title": "Old Title"})
    repo.update_document("doc-1", {"title": "New Title", "id": "doc-1"})
    doc = repo.read_document("doc-1")
    assert doc is not None, "Expected to find document with id 'doc-1'"
    assert doc["title"] == "New Title"

def test_delete_document(repo: DocumentRepository) -> None:
    repo.create_document("doc-1", {"title": "To be deleted"})
    repo.delete_document("doc-1")
    doc = repo.read_document("doc-1")
    
    assert doc is None
