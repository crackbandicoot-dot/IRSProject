from typing import Dict, Optional, List
from pymongo import MongoClient

class DocumentRepository:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", db_name: str = "irs_db") -> None:
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]
        self._documents = self._db["documents"]

    def create_document(self, doc_id: str, document_data: dict) -> None:
        """Create or insert a new document."""
        document_data["_id"] = doc_id
        if "id" not in document_data:
            document_data["id"] = doc_id
        self._documents.insert_one(document_data)

    def read_document(self, doc_id: str) -> Optional[dict]:
        """Read a document by its ID."""
        doc = self._documents.find_one({"_id": doc_id})
        if doc and "_id" in doc:
            doc.pop("_id")
        return doc

    def update_document(self, doc_id: str, document_data: dict) -> None:
        """Update an existing document."""
        self._documents.update_one({"_id": doc_id}, {"$set": document_data})

    def delete_document(self, doc_id: str) -> None:
        """Delete a document by its ID."""
        self._documents.delete_one({"_id": doc_id})
