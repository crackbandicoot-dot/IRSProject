import typing
import pytest
from DocumentEmbeddingRepository.DocumentEmbeddingRepository import DocumentEmbeddingRepository
from qdrant_client import QdrantClient
from qdrant_client.http import models

@pytest.fixture
def real_repo() -> typing.Generator[DocumentEmbeddingRepository, None, None]:
    repo = DocumentEmbeddingRepository(collection_name="test_embeddings")
    if repo.client.collection_exists(repo.collection_name):
        repo.client.delete_collection(collection_name=repo.collection_name)
    
    repo.client.create_collection(
        collection_name=repo.collection_name,
        vectors_config={
            "cosine": models.VectorParams(size=4, distance=models.Distance.COSINE),
            "euclidean": models.VectorParams(size=4, distance=models.Distance.EUCLID),
            "dot": models.VectorParams(size=4, distance=models.Distance.DOT),
            "manhattan": models.VectorParams(size=4, distance=models.Distance.MANHATTAN)
        }
    )
    yield repo
    
    # Cleanup after test
    repo.client.delete_collection(collection_name=repo.collection_name)

def test_integration_save_and_get(real_repo: DocumentEmbeddingRepository) -> None:
    doc_id = "integration_doc_1"
    embedding = [0.1, 0.2, 0.3, 0.4]
    real_repo.save(doc_id, embedding)
    retrieved = real_repo.get(doc_id)
    assert retrieved is not None
    for r, e in zip(retrieved, embedding):
        assert abs(r - e) < 1e-6

def test_integration_delete(real_repo: DocumentEmbeddingRepository) -> None:
    doc_id = "integration_doc_2"
    embedding = [0.5, 0.6, 0.7, 0.8]
    real_repo.save(doc_id, embedding)
    assert real_repo.get(doc_id) is not None
    real_repo.delete(doc_id)
    assert real_repo.get(doc_id) is None

def test_integration_semantic_search(real_repo: DocumentEmbeddingRepository) -> None:
    base_embedding = [1.0, 0.0, 0.0, 0.0]
    real_repo.save("exact_match", base_embedding)
    real_repo.save("close_match", [0.9, 0.1, 0.0, 0.0])
    real_repo.save("far_match", [0.0, 1.0, 0.0, 0.0])
    
    results = real_repo.semantic_search(query_embedding=base_embedding, limit=2, metric="cosine")
    
    assert len(results) == 2
    assert results[0].document_id == "exact_match"
    assert results[1].document_id == "close_match"
