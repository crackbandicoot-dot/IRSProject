from .query_node import QueryNode

class TermNode(QueryNode):

    @property
    def term(self)->str:
        return self._term
    
    def  __init__(self,term:str) -> None:
        self._term = term
        
    