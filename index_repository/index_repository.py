from .index_repository_impl import IndexRepository
from contracts.indexed_document.indexed_document import IndexedDocument
from typing import List, Dict, Optional
from contracts.either import railway
_instance = IndexRepository()

def create_index(doc_id: str, term_weights: Dict[str, float]) -> None:
    _instance.create_index(doc_id, term_weights)

def read_index(doc_id: str) -> Optional[IndexedDocument]:
    return _instance.read_index(doc_id)

def update_index(doc_id: str, term_weights: Dict[str, float]) -> None:
    _instance.update_index(doc_id, term_weights)

def delete_index(doc_id: str) -> None:
    _instance.delete_index(doc_id)

@railway
def get_relevant_indexes(raw_query: str) -> List[IndexedDocument]:
    return _instance.get_relevant_indexes(raw_query)