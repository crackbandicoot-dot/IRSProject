from .QueryNode import QueryNode

class TermNode(QueryNode):

    @property
    def term(self)->str:
        return self._term
    
    def  __init__(self,term:str):
        self._term = term
        
    