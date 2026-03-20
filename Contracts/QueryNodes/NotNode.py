from .QueryNode import QueryNode

class NotNode(QueryNode):
    @property
    def child(self)->QueryNode:
        return self._child

    def __init__(self, child: QueryNode) -> None:
        self._child = child
    