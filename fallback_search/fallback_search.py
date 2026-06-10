from contracts.settings import Config
from contracts.rich_result import RichResult
from typing import List
from ddgs import DDGS
from contracts.either import railway
@railway
def search(query: str, config: Config) -> List[RichResult]:
    results = []
    with DDGS() as duck_duck_go:
        
        # We'll use config.min_score as fallback score, and we can fetch at most config.top_k results
        for r in duck_duck_go.text(query, max_results=config.top_k):
            results.append(RichResult(
                title=r["title"],
                snippet=r["body"][:min(len(r["body"]),150)],
                score=config.min_score,
                url=r["href"]
            ))
    return results