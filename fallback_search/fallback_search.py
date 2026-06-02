from contracts.settings import Config
from contracts.search_results.search_result import SearchResult
from typing import List
from ddgs import DDGS

def search(query: str, config: Config) -> List[SearchResult]:
    results = []
    with DDGS() as ddgs:
        # We'll use config.min_score as fallback score, and we can fetch at most config.top_k results
        for r in ddgs.text(query, max_results=config.top_k):
            results.append(SearchResult(document_id=r["href"], score=config.min_score))
    return results