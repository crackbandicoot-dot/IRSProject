# Instantiate any underlying parser/tokenizer classes here at module level if needed
from .QueryParser import QueryParser
from Contracts.QueryNodes import QueryNode
def parse(raw_query: str) -> QueryNode:
    parser = QueryParser(raw_query)
    return parser.parse()
