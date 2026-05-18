from .DocumentRepository import DocumentRepository
from typing import Optional

_instance = DocumentRepository()

def create_document(doc_id: str, document_data: dict) -> None:
    _instance.create_document(doc_id, document_data)

def read_document(doc_id: str) -> Optional[dict]:
    return _instance.read_document(doc_id)

def update_document(doc_id: str, document_data: dict) -> None:
    _instance.update_document(doc_id, document_data)

def delete_document(doc_id: str) -> None:
    _instance.delete_document(doc_id)
