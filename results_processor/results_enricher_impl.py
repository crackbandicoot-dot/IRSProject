from pymongo import MongoClient
from contracts.search_results.search_result import SearchResult
from contracts.rich_result import RichResult
from typing import List
class ResultsEnricher:
    def __init__(self,connection_string: str = "mongodb://localhost:27017/", db_name: str = "irs_db") -> None:
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self._documents = self.db["documents"]
        self.w = 0.5 # Weight for fuzzy score in the combined score (0.5 means equal weight to both)

    def combine(self, fuzzy_results: List[SearchResult],semantic_results: List[SearchResult]) -> List[SearchResult]:
        # Dictionary stores: {document_id: search_result_object}
        merged = {}
        
        # 1. Process fuzzy results (updates score in-place)
        for result in fuzzy_results:
            result.score *= self.w
            merged[result.document_id] = result
            
        # 2. Process semantic results
        w_semantic = 1.0 - self.w
        for result in semantic_results:
            if result.document_id in merged:
                # Add to the existing object's score
                merged[result.document_id].score += w_semantic * result.score
            else:
                # Update score and store the object
                result.score *= w_semantic
                merged[result.document_id] = result
        return list(merged.values())
    
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
     