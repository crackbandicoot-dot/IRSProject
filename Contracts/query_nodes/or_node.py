from .query_node import QueryNode
class OrNode(QueryNode):
    @property
    def left(self)-> QueryNode:
        return self._left
    
    @property
    def right(self)-> QueryNode:
        return self._right

    def __init__(self, left: QueryNode, rigth: QueryNode) -> None:
        self._left =left
        self._right = rigth
   