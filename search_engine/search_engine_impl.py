from contracts.query_nodes import QueryNode,AndNode, OrNode, NotNode, HedgeNode, TermNode
from contracts.search_results.search_result import SearchResult
from contracts.indexed_document.indexed_document import IndexedDocument
from contracts.settings import Config
from typing import List, Tuple
import math
class SearchEngine:
  
    def search(self, index_results: List[IndexedDocument], parsed_query: QueryNode, 
               config: Config) -> List[SearchResult]:
        
        search_results = []
        for document in index_results:
            if len(search_results)>=config.top_k:
                break
            degree = self._evaluate_node(parsed_query,document)

            if degree >= config.min_score:
                search_results.append(SearchResult(document.id,degree))
        return search_results
    def _evaluate_node(self, query_node: QueryNode, 
                       document: IndexedDocument,
                       ) ->  float:
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
    
    def _evaluate_and(self, and_node: AndNode, document: IndexedDocument,
                ) -> float:
        left = self._evaluate_node(and_node.left,document)
        right = self._evaluate_node(and_node.right,document)
        return min(left, right)
    def _evaluate_or(self, or_node: OrNode, document: IndexedDocument,
        ) -> float:
        left = self._evaluate_node(or_node.left,document)
        right = self._evaluate_node(or_node.right,document)
        return max(left, right)
    def _evaluate_not(self, not_node: NotNode, document: IndexedDocument,
                    ) -> float:
        degree = self._evaluate_node(not_node.child,document)
        return 1-degree
    def _evaluate_hedge(self, hedge_node: HedgeNode, document: IndexedDocument,
                        ) -> float:
        degree = self._evaluate_node(hedge_node.child, document)
        if hedge_node.hedge_keyword == "IMPORTANT":
           return self._mu_important(degree)
        exponent = self._resolve_hedge_exponent(hedge_node.hedge_keyword)
        return degree ** exponent

    def _resolve_hedge_exponent(self, hedge_keyword: str) -> float:
        hedges = {
            "VERY": 2.0,
            "EXTREMELY": 3.0,
            "SLIGHTLY": 0.5,
            "SOMEWHAT": 0.75,
            "MILDLY": 0.8,
            
        }
        return hedges.get(hedge_keyword, 1.0)

    def _evaluate_term(self, term_node: TermNode, document: IndexedDocument) -> float:
        return document[term_node]
    
    @staticmethod
    def _mu_important(x: float, i: float = 0.7, j: float = 1.0,
                       k: float = 0.000083) -> float:
        """Convert raw term weight to 'important' compatibility (paper formula)."""
        if i <= x <= j:
            return 1.0
        boundary = i if x < i else j
        diff = x - boundary
        return math.exp(diff * diff * math.log(k))
