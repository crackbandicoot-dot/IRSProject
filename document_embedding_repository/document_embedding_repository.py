from typing import List, Optional

from contracts.errors import AppError
from document_embedding_repository.document_embedding_repository_impl import DocumentEmbeddingRepository
from contracts.search_results.search_result import SearchResult
from contracts.either import Either, railway
from shared.logger import get_logger

_repository = DocumentEmbeddingRepository()
_logger = get_logger(__name__)

@railway
def save(doc_id: str, embedding: List[float]) -> None:
    _logger.info(f"Saving embedding for doc_id: {doc_id}")
    _repository.save(doc_id, embedding)
    

@railway
def delete(doc_id: str) -> None:
    _logger.info(f"Deleting embedding for doc_id: {doc_id}")
    _repository.delete(doc_id)
  

@railway
def get(doc_id: str) -> Optional[List[float]]:
    _logger.info(f"Tryng to get raw embedding from document with id{doc_id}")
    return _repository.get(doc_id)

@railway
def semantic_search(query_embedding_either: Either[AppError, List[float]], 
    limit: int = 10, metric: str = "cosine") -> List[SearchResult]:
    _logger.info("Tryng to perform semantic search with query embedding")
    query_embedding = query_embedding_either.unwrap()
    return _repository.semantic_search(query_embedding, limit, metric)
