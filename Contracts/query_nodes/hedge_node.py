from .query_node import QueryNode

class HedgeNode(QueryNode):
    @property
    def hedge_keyword(self)-> str:  
        return self._hedge_keyword
    @property
    def child(self)-> QueryNode:
        return self._child
    
    def __init__(self, hedge_keyword: str, child: QueryNode) -> None:
        self._hedge_keyword = hedge_keyword
        self._child = child
    