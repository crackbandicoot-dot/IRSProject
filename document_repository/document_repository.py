from .document_repository_impl import DocumentRepository
from contracts.either import railway
from shared.logger import get_logger
from typing import Optional
_instance = DocumentRepository()
_logger = get_logger(__name__)

@railway
def create_document(doc_id: str, document_data: dict) ->None:
    """Creates or insert a new document."""
    _logger.info(f"Tryng to create document with id {doc_id}")
    _instance.create_document(doc_id, document_data)
    
@railway
def read_document(doc_id: str) -> Optional[dict]:
    """Read a document by its ID."""
    _logger.info(f"Tryng to read document with id '{doc_id}'")
    return _instance.read_document(doc_id)

@railway
def update_document(doc_id: str, document_data: dict,upsert=False) -> None:
    """Update an existing document, or creates one if upsert is set to True(the default is setted to False)"""
    _logger.info(f"Tryng to update document with id {doc_id}")
    _instance.update_document(document_data,upsert)
    
@railway
def delete_document(doc_id: str) -> None:
    """Delete a document by its ID."""
    _logger.info(f"Tryng to delete document  with id {doc_id}")
    _instance.delete_document(doc_id)
