# Instantiate any underlying enricher/formatter classes here at module level if needed
from .results_enricher_impl import ResultsEnricher
from contracts.search_results.search_result import SearchResult
from contracts.rich_result.rich_result import RichResult, RAGResult
from contracts.settings import Config
from typing import List, Iterable, Tuple
from contracts.either import railway, Either
from contracts.errors import AppError
from shared.logger import get_logger

_enricher = ResultsEnricher()  # This will connect to MongoDB and be ready to enrich results
_logger = get_logger(__name__)

@railway 
def enrich(raw_search_results_either: Either[AppError, Iterable[SearchResult]],
           documents_either: Either[AppError, List[dict]]) -> Tuple[List[RichResult], List[RAGResult]]:
   _logger.info("Enriching search results")
   return _enricher.enrich(raw_search_results_either.unwrap(), documents_either.unwrap())

@railway
def combine(fuzzy_results_either: Either[AppError, Iterable[SearchResult]],
   semantic_results_either: Either[AppError, Iterable[SearchResult]],
   config: Config) -> Iterable[SearchResult]:
    _logger.info("Combining fuzzy and semantic search results")
    fuzzy_results = fuzzy_results_either.unwrap()
    semantic_results = semantic_results_either.unwrap()
    return _enricher.combine(fuzzy_results, semantic_results, config)

@railway
def prepare_context(query:str,rag_results_either: Either[AppError, List[RAGResult]]) -> str:
    """Prepare context string from RAG results."""
    rag_results = rag_results_either.unwrap()
    context_parts = []
    for res in rag_results:
        context_parts.append(f"Source: {res['title']} ({res['url']})\nContent: {res['content']}")
    return "\n\n---\n\n".join(context_parts)

@railway
def prepare_context_from_rich(query:str,rich_results_either: Either[AppError, List[RichResult]]) -> str:
    """Prepare context string from Rich results (UI snippets)."""
    rich_results = rich_results_either.unwrap()
    context_parts = []
    for res in rich_results:
        context_parts.append(f"Source: {res['title']} ({res['url']})\nContent: {res['snippet']}")
    return "\n\n---\n\n".join(context_parts)

@railway
def get_ui_results(enriched_either: Either[AppError, Tuple[List[RichResult], List[RAGResult]]]) -> List[RichResult]:
    """Extract UI results from enriched tuple."""
    ui_results, _ = enriched_either.unwrap()
    return ui_results

@railway
def get_rag_results(enriched_either: Either[AppError, Tuple[List[RichResult], List[RAGResult]]]) -> List[RAGResult]:
    """Extract RAG results from enriched tuple."""
    _, rag_results = enriched_either.unwrap()
    return rag_results
