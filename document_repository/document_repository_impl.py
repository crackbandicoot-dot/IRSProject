from typing import Optional
from pymongo import MongoClient
from shared.logger import get_logger

logger = get_logger(__name__)
import os
class DocumentRepository:
    def __init__(self, connection_string: Optional[str] = None,
                db_name: Optional[str] = None, collection_name: str = "documents") -> None:
        self.db_name = db_name or os.getenv("MONGODB_DB", "irs_db")
        self.collection_name = collection_name
        conn_str = connection_string or os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self._client = MongoClient(conn_str)
        self._db = self._client[self.db_name]
        self._documents = self._db[collection_name]

    def create_document(self, doc_id: str, document_data: dict) -> None:
        document_data["_id"] = doc_id
        if "id" not in document_data:
            document_data["id"] = doc_id
        result = self._documents.insert_one(document_data)
        if not result.inserted_id:
            logger.warning(f"cannot instert document '{document_data}' and id '{doc_id}'")
            

    def read_document(self, doc_id: str) -> Optional[dict]:
        doc = self._documents.find_one({"_id": doc_id})
        if doc and "_id" in doc:
            doc.pop("_id")
            return doc
        logger.warning(f"Document with id '{doc_id}' not found in collection '{self.collection_name}'.")

    def read_documents(self, doc_ids: list[str]) -> list[dict]:
        """Read multiple documents by their IDs."""
        docs = list(self._documents.find({"_id": {"$in": doc_ids}}))
        doc_map = {doc["_id"]: doc for doc in docs}
        result = []
        for doc_id in doc_ids:
            if doc_id in doc_map:
                doc = doc_map[doc_id]
                if "_id" in doc:
                    doc.pop("_id")
                result.append(doc)
            else:
                logger.warning(f"Document with id '{doc_id}' not found.")
        return result
        
    def update_document(self,document_data: dict,upsert:bool) -> None:
        result = self._documents.update_one({"_id": document_data["doc_id"]}, {"$set": document_data},upsert)
        if result.modified_count==0:
            logger.warning("Nothing was modified during update operation.")
        
    def delete_document(self, doc_id: str) -> None:
        result = self._documents.delete_one({"_id": doc_id})
        if result.deleted_count==0:
            logger.warning(f"Nothing was deleted during delete operation for document id '{doc_id}'.")
    