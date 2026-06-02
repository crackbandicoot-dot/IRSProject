# Instantiate any underlying search/ranking classes here at module level if needed
from .search_engine_impl import SearchEngine
from contracts.query_nodes.query_node import QueryNode
from contracts.indexed_document.indexed_document import IndexedDocument
from contracts.search_results.search_result import SearchResult
from contracts.settings import Config
from typing import List
from contracts.either import railway,Either
from contracts.errors import AppError
from shared.logger import get_logger

_logger = get_logger(__name__)
_search_engine = SearchEngine()

@railway
def search(parsed_query_either: Either[AppError,QueryNode],
        relevant_indexes_either: Either[AppError,List[IndexedDocument]],
        config: Config
        ) -> List[SearchResult]:
    _logger.info("Tryng to execute search for query")
    parsed_query = parsed_query_either.unwrap()
    relevant_indexes = relevant_indexes_either.unwrap()
    return _search_engine.search(relevant_indexes,parsed_query,config)
