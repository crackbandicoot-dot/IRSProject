# Instantiate any underlying enricher/formatter classes here at module level if needed
from .results_enricher_impl import ResultsEnricher
from contracts.search_results.search_result import SearchResult
from contracts.rich_result.rich_result import RichResult
from contracts.settings import Config
from typing import List,Iterable
from contracts.either import railway,Either
from contracts.errors import AppError
from shared.logger import get_logger

_enricher = ResultsEnricher()  # This will connect to MongoDB and be ready to enrich results
_logger = get_logger(__name__)

@railway 
def enrich(raw_search_results_either: Either[AppError,Iterable[SearchResult]]) -> List[RichResult]:
   _logger.info("Enriching search results")
   raw_search_results = raw_search_results_either.unwrap()
   return _enricher.enrich_results(raw_search_results)

@railway
def combine(fuzzy_results_either: Either[AppError,Iterable[SearchResult]],
   semantic_results_either: Either[AppError,Iterable[SearchResult]],
   config: Config) -> Iterable[SearchResult]:
    _logger.info("Combining fuzzy and semantic search results")
    fuzzy_results = fuzzy_results_either.unwrap()
    semantic_results = semantic_results_either.unwrap()
    return _enricher.combine(fuzzy_results, semantic_results, config)
