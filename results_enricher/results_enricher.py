# Instantiate any underlying enricher/formatter classes here at module level if needed
from .results_enricher_impl import ResultsEnricher
from contracts.search_results.search_result import SearchResult
from contracts.rich_result.rich_result import RichResult
from typing import List
from contracts.either import railway,Either
from contracts.errors import AppError

_enricher = ResultsEnricher()  # This will connect to MongoDB and be ready to enrich results
@railway 
def enrich(raw_search_results_either: Either[AppError,List[SearchResult]]) -> List[RichResult]:
   raw_search_results = raw_search_results_either.unwrap()
   return _enricher.enrich_results(raw_search_results)
