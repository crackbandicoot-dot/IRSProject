import re
from typing import List, Dict, Optional
from pymongo import MongoClient
from contracts.indexed_document.indexed_document import IndexedDocument
from shared.logger import get_logger
logger = get_logger(__name__)
import os
class IndexRepository:
    def __init__(self, connection_string: Optional[str] = None,
         db_name: Optional[str] = None, collection_name: str = "postings") -> None:
        self.db_name = db_name or os.getenv("MONGODB_DB", "irs_db")
        self.collection = collection_name
        conn_str = connection_string or os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
        self._client = MongoClient(conn_str)
        self._db = self._client[self.db_name]
        self._postings = self._db[collection_name]

    def create_index(self, index_data: list) -> None:
        """Create or insert an index for a document."""
        with self._client.start_session() as session:
            with session.start_transaction():
                result = self._postings.insert_many(index_data)
                if len(result.inserted_ids)!= len(index_data):
                    logger.warning(f"error inserting index_data: '{index_data}'")
            
    def read_index(self, doc_id: str) -> Optional[IndexedDocument]:
        """Read all index postings for a given document."""
        postings_cursor = self._postings.find({"doc_id": doc_id})
        
        doc_weights: dict = {}
        for posting in postings_cursor:
            doc_id = posting["doc_id"]
            term = posting["term"]
            weight = posting["weight"]
            if doc_id not in doc_weights:
                doc_weights[doc_id] = {}
            doc_weights[doc_id][term] = weight

        if not doc_weights:
            logger.warning(f"document with id {doc_id} is an empty document")
            return None
            
        return IndexedDocument(doc_id=doc_id, term_weights=doc_weights)

    def update_index(self,index_data:dict) -> None:
        """Update an index by replacing existing terms for a document with new ones."""
        with self._client.start_session() as session:
            with session.start_transaction():
                result = self._postings.update_many({"doc_id": index_data["doc_id"]},index_data)
                if result.modified_count!= len(index_data):
                    logger.warning(f"index data '{index_data}' wasn't updated")
                
    def delete_index(self, doc_id: str) -> None:
        """Delete all index postings for a given document."""
        with self._client.start_session() as session:
            with session.start_transaction():
               result = self._postings.delete_many({"doc_id": doc_id})
               if result.deleted_count==0:
                   logger.warning(f"doc_id '{doc_id}' was'nt deleted")
    
    
    def get_relevant_indexes(self, raw_query: str) -> List[IndexedDocument]:
        terms = self._extract_terms(raw_query)
        if not terms:
            logger.warning("empty query")
            return []

        with self._postings.find({"term": {"$in": terms}}) as postings_cursor:
            doc_weights: dict = {}
            for posting in postings_cursor:
                doc_id = posting["doc_id"]
                term = posting["term"]
                weight = posting["weight"]
                if doc_id not in doc_weights:
                    doc_weights[doc_id] = {}
                doc_weights[doc_id][term] = weight

        return [IndexedDocument(doc_id, weights) for doc_id, weights in doc_weights.items()]

    def _extract_terms(self, raw_query: str) -> List[str]:
        # Terms in the query language are lowercase words.
        # Operators (AND, OR, NOT) and hedge keywords (VERY, FAIRLY) are uppercase.
        tokens = re.findall(r'\b[a-zA-Z]+\b', raw_query)
        return [t for t in tokens if t.islower()]