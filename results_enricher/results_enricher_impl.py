from pymongo import MongoClient
from contracts.search_results.search_result import SearchResult
from contracts.rich_result import RichResult
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
                rich_results.append(RichResult(
                    title=doc.get("title", ""),
                    snippet=doc.get("content", "")[:150],
                    score=result.score
                ))
        return rich_results
     