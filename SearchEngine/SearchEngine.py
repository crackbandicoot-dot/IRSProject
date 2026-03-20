from Contracts.QueryNodes import QueryNode,AndNode, OrNode, NotNode, HedgeNode, TermNode
from Contracts.SearchResults import SearchResult
from Contracts.IndexedDocument import IndexedDocument
from typing import List, Tuple
class SearchEngine:
  
    #TODO : implement hedge evaluation
    #TODO :Make the engine extensible
    def search(self, index_results: List[IndexedDocument], parsed_query: QueryNode) -> List[SearchResult]:
        search_results = []
        for document in index_results:
            min,max  = self._evaluate_node(parsed_query,document)
            if isinstance(parsed_query, AndNode):
                search_results.append(SearchResult(document.id,0.7*min+0.3*max))
            elif isinstance(parsed_query,OrNode):
                search_results.append(SearchResult(document.id,0.3*min+0.7*max))
            else: 
                search_results.append(SearchResult(document.id,max))    
        return search_results
    def _evaluate_node(self, query_node: QueryNode, document: IndexedDocument) -> Tuple[float, float]:
        if isinstance(query_node, AndNode):
            return self._evaluate_and(query_node,document)
        if isinstance(query_node, OrNode):
            return self._evaluate_or(query_node,document)
        if isinstance(query_node, NotNode):
            return self._evaluate_not(query_node,document)
        if isinstance(query_node, HedgeNode):
            return self._evaluate_hedge(query_node,document)
        if isinstance(query_node, TermNode):
            return self._evaluate_term(query_node,document)
        raise ValueError("Unknown query node type")
    
    def _evaluate_and(self, and_node: AndNode, document: IndexedDocument) -> Tuple[float, float]:
        min_left, max_left = self._evaluate_node(and_node.left,document)
        min_right, max_right = self._evaluate_node(and_node.right,document)
        return min(min_left, min_right), max(max_left, max_right)
    def _evaluate_or(self, or_node: OrNode, document: IndexedDocument) -> Tuple[float, float]:
        min_left, max_left = self._evaluate_node(or_node.left,document)
        min_right, max_right = self._evaluate_node(or_node.right,document)
        return min(min_left, min_right), max(max_left, max_right)
    def _evaluate_not(self, not_node: NotNode, document: IndexedDocument) -> Tuple[float, float]:
        min,max = self._evaluate_node(not_node.child,document)
        return 1-max,1-min
    def _evaluate_hedge(self, hedge_node: HedgeNode, document: IndexedDocument) -> Tuple[float, float]:
        raise NotImplementedError("Hedge evaluation not implemented yet")
    def _evaluate_term(self, term_node: TermNode, document: IndexedDocument) -> Tuple[float, float]:
        degree_of_belong = document[term_node]
        return degree_of_belong, degree_of_belong
