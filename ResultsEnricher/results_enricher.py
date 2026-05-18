# Instantiate any underlying enricher/formatter classes here at module level if needed
from .ResultsEnricher import ResultsEnricher
from Contracts.SearchResults import SearchResult
from Contracts.RichResult import RichResult
from typing import List

_enricher = ResultsEnricher()  # This will connect to MongoDB and be ready to enrich results
def enrich(raw_search_results: List[SearchResult]) -> List[RichResult]:
   return _enricher.enrich_results(raw_search_results)
