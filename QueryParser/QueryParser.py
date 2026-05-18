from Contracts.QueryNodes import AndNode,TermNode, HedgeNode,QueryNode,OrNode,NotNode
from Errors.QueryError.query_error import QueryError

class QueryParser:
    
    def __init__(self, raw_query: str) -> None:
        self.current = ""
        self.index = -1
        self.query_tokens = raw_query.replace("("," ( ").replace(")"," ) ").split()
        self._next()
    def parse(self) -> QueryNode:
        query_node= self._or()
        if self.current!="\0":
            raise QueryError(self.index+1, "Can't parse query unexpected end of query. " \
            "Hint: between basic terms such as lower case words or parenthesized expressions " \
            "it should be an AND/OR operator")
        return query_node
             
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
            raise QueryError(self.index+1, "Unexpected end of query")
        if self.current.islower():
            term = self.current
            self._next()
            return TermNode(term)
        if self.current =="(": # Grouping expressions
            self._next()
            query_exp = self._or()
            if self.current == ")":
                self._next()
                return query_exp
            raise QueryError(self.index+1, 'Expected ")"')

        raise QueryError(self.index+1, f'Word "{self.current}" is invalid')
    
    def _next(self) -> None:
        token = self._peek(1)
        self.index+=1
        self.current = token

    def _peek(self,offset:int) -> str:
        if self.index+offset>len(self.query_tokens)-1:
            return "\0"
        return self.query_tokens[self.index+offset]
    
    