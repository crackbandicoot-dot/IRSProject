import heapq
from pymongo import MongoClient
from contracts.search_results.search_result import SearchResult
from contracts.rich_result import RichResult
from typing import Iterable, List

from contracts.settings import Config
class ResultsEnricher:
    def __init__(self,connection_string: str = "mongodb://localhost:27017/", db_name: str = "irs_db") -> None:
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]
        self._documents = self.db["documents"]
        self.w = 0.5 # Weight for fuzzy score in the combined score (0.5 means equal weight to both)

    def combine(self, fuzzy_results: Iterable[SearchResult],
                semantic_results: Iterable[SearchResult],
                config:Config
                ) -> Iterable[SearchResult]:
        
        combined_scores = {}
        for res in fuzzy_results:
            combined_scores[res.document_id] = combined_scores.get(res.document_id, 0.0) + self.w * res.score
            
        for res in semantic_results:
            combined_scores[res.document_id] = combined_scores.get(res.document_id, 0.0) + (1.0 - self.w) * res.score
            
        heap = []
        for doc_id, score in combined_scores.items():
            if score >= config.min_score:
                if len(heap) < config.top_k:
                    heapq.heappush(heap, (score, doc_id))
                else:
                    heapq.heappushpop(heap, (score, doc_id))
                    
        return [
            SearchResult(document_id=doc_id, score=score) 
            for score, doc_id in sorted(heap, key=lambda x: x[0], reverse=True)
        ]
        
    
    def enrich_results(self,raw_search_results: Iterable[SearchResult]]) -> List[RichResult]:
        rich_results: List[RichResult] = []
        for result in raw_search_results:
            doc = self._documents.find_one({"_id": result.document_id})
            if doc:
                content:str =doc.get("content", "")
                rich_results.append(RichResult(
                    title=doc.get("title", ""),
                    snippet=content[:min(len(content), 650)],
                    score=result.score,
                    url = doc.get("url","")
                ))
        return rich_results
     