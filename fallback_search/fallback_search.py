from contracts.settings import Config
from contracts.search_results.search_result import SearchResult
from typing import List
from ddgs import DDGS
from contracts.either import railway
@railway
def search(query: str, config: Config) -> List[SearchResult]:
    results = []
    with DDGS() as duck_duck_go:
        
        # We'll use config.min_score as fallback score, and we can fetch at most config.top_k results
        for r in duck_duck_go.text(query, max_results=config.top_k):
            results.append(SearchResult(document_id=r["href"], score=config.min_score))
    return results