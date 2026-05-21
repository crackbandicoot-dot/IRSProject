from .query_node import QueryNode


class AndNode(QueryNode):
    @property
    def left(self)-> QueryNode:
        return self._left
    
    @property
    def right(self)-> QueryNode:
        return self._rigth

    def __init__(self, left: QueryNode, rigth: QueryNode) -> None:
        self._left =left
        self._rigth = rigth
        