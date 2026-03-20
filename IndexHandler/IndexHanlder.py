import re
from typing import List
from pymongo import MongoClient
from Contracts.IndexedDocument import IndexedDocument


class IndexHandler:
    def __init__(self, connection_string: str = "mongodb://localhost:27017/", db_name: str = "irs_db") -> None:
        self._client = MongoClient(connection_string)
        self._db = self._client[db_name]
        self._postings = self._db["postings"]

    def get_relevant_indexes(self, raw_query: str) -> List[IndexedDocument]:
        terms = self._extract_terms(raw_query)
        if not terms:
            return []

        postings_cursor = self._postings.find({"term": {"$in": terms}})

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
        # Operators (AND, OR, NOT) and hedge keywords (VERY, FAIRLY…) are uppercase.
        tokens = re.findall(r'\b[a-zA-Z]+\b', raw_query)
        return [t for t in tokens if t.islower()]