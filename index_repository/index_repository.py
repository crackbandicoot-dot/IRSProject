from .index_repository_impl import IndexRepository
from contracts.indexed_document.indexed_document import IndexedDocument
from typing import List, Optional
from contracts.either import railway
from shared.logger import get_logger

_instance = IndexRepository()
_logger = get_logger(__name__)

@railway
def create_index(index_data:list) -> None:
    if len(index_data)==0:
        _logger.warning(f"Trying to create an index with empty index_data: '{index_data}'")
    else:
        _logger.info(f"Tryng to index for doc with id {index_data[0]["doc_id"]}")
    _instance.create_index(index_data)

@railway
def read_index(doc_id: str) -> Optional[IndexedDocument]:
    _logger.info(f"Tryng to read index for doc_id: {doc_id}")
    return _instance.read_index(doc_id)

@railway
def update_index(index_data:dict) -> None:
    _logger.info(f"Tryng to update index for doc with id {index_data["doc_id"]}")
    _instance.update_index(index_data)

@railway
def delete_index(doc_id: str) -> None:
    _logger.info(f"Deleting index for doc_id: {doc_id}")
    _instance.delete_index(doc_id)
    
@railway
def get_relevant_indexes(raw_query: str) -> List[IndexedDocument]:
    _logger.info(f"Tryng to get relevant indexes for query{raw_query}")
    return _instance.get_relevant_indexes(raw_query)