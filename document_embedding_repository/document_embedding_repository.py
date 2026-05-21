from typing import List, Optional

from document_embedding_repository.document_embedding_repository_impl import DocumentEmbeddingRepository
from contracts.search_results.search_result import SearchResult

_repository = DocumentEmbeddingRepository()

def save(doc_id: str, embedding: List[float]) -> None:
    return _repository.save(doc_id, embedding)

def delete(doc_id: str) -> None:
    return _repository.delete(doc_id)

def get(doc_id: str) -> Optional[List[float]]:
    return _repository.get(doc_id)

def semantic_search(query_embedding: List[float], limit: int = 10, metric: str = "cosine") -> List[SearchResult]:
    return _repository.semantic_search(query_embedding, limit, metric)
