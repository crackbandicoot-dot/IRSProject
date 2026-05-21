# Instantiate any underlying parser/tokenizer classes here at module level if needed
from .query_parser_impl import QueryParser
from contracts.query_nodes import QueryNode
from contracts.either import railway
@railway
def parse(raw_query: str) -> QueryNode:
    parser = QueryParser(raw_query)
    return parser.parse()
