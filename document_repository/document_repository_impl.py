from typing import Optional
from pymongo import MongoClient
from shared.logger import get_logger

logger = get_logger(__name__)
class DocumentRepository:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", db_name: str = "irs_db",collection_name="documents") -> None:
        self.db_name =db_name
        self.collection_name = collection_name
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]
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
        
    def update_document(self,document_data: dict,upsert:bool) -> None:
        result = self._documents.update_one({"_id": document_data["doc_id"]}, {"$set": document_data},upsert)
        if result.modified_count==0:
            logger.warning("Nothing was modified during update operation.")
        
    def delete_document(self, doc_id: str) -> None:
        result = self._documents.delete_one({"_id": doc_id})
        if result.deleted_count==0:
            logger.warning(f"Nothing was deleted during delete operation for document id '{doc_id}'.")
    