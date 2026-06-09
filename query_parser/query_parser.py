# Instantiate any underlying parser/tokenizer classes here at module level if needed
from .query_parser_impl import QueryParser
from contracts.query_nodes import QueryNode
from contracts.either import railway
from shared.logger import get_logger
from shared.constants import TOKEN_REGEX
import re
_logger = get_logger(__name__)

@railway
def parse(raw_query: str) -> QueryNode:
    _logger.info(f"Tryng to parse query: {raw_query}")
    parser = QueryParser(raw_query)
    return parser.parse()

@railway
def strip_operators(raw_query:str)->str:
    return " ".join(re.findall(TOKEN_REGEX, raw_query))

