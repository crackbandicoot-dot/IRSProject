from pymongo import MongoClient
from Contracts.SearchResults import SearchResult
from Contracts.RichResult import RichResult
from typing import List
class ResultsEnricher:
    def __init__(self,connection_string: str = "mongodb://localhost:27017/", db_name: str = "irs_db") -> None:
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self._documents = self.db["documents"]

    def enrich_results(self, raw_search_results: List[SearchResult]) -> List[RichResult]:
        rich_results: List[RichResult] = []
        for result in raw_search_results:
            doc = self._documents.find_one({"_id": result.document_id})
            if doc:
                rich_result = {
                    "title": doc["title"],
                    "snippet": doc["content"][:150],
                    "score": result.score,
                }
                rich_results.append(rich_result)
        return rich_results
     