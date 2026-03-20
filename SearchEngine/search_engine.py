# Instantiate any underlying search/ranking classes here at module level if needed
from .SearchEngine import SearchEngine
from Contracts.QueryNodes import QueryNode
from Contracts.IndexedDocument import IndexedDocument
from Contracts.SearchResults import SearchResult
from typing import List
def search(parsed_query: QueryNode, relevant_indexes: List[IndexedDocument]) -> List[SearchResult]:
    _search_engine = SearchEngine()
    return _search_engine.search(relevant_indexes,parsed_query)
