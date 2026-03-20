from Contracts.QueryNodes import AndNode,TermNode, HedgeNode,QueryNode,OrNode,NotNode

class QueryParser:
    
    def __init__(self, raw_query: str) -> None:
        self.index = -1
        self.query_tokens = raw_query.split()
        self._next()
        
    def parse(self) -> QueryNode:
        return self._or()

    def _or(self)->QueryNode:
        left = self._and()
        while self.current=="OR":
            self._next()
            rigth = self._and()
            left = OrNode(left,rigth)
        return left
    
    def _and(self)->QueryNode:
        left = self._unary()
        while self.current=="AND":
            self._next()
            rigth = self._unary()
            left = AndNode(left,rigth)
        return left
        
   
    def _unary(self) -> QueryNode:
        if self.current == "NOT":
            self._next()
            return NotNode(self._unary())
        elif self.current.isupper() and self.current not in ["AND","OR" ]:
            hedge = self.current
            self._next()
            return HedgeNode(hedge,self._unary())
        return self._primary()
    
    def _primary(self) -> QueryNode:
        
        if self.current == "\0":
            raise RuntimeError(f"Unexpected end of query on column {self.index+1}")
        if self.current.islower():
            term = self.current
            self._next()
            return TermNode(term)
        if self.current =="(": # Grouping expressions
            self._next()
            query_exp = self._and()
            if self.current == ")":
                return query_exp
            raise RuntimeError(f"Invalid query, expected ')' on column {self.index+1}")
        raise RuntimeError(f"Unexpected query token on column {self.index+1}")
    def _next(self) -> None:
        if self.index >= len(self.query_tokens)-1:
            self.current="\0"
            return
        self.index+=1
        self.current = self.query_tokens[self.index]
    
    