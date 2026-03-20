from .IndexHanlder import IndexHandler
from Contracts.IndexedDocument import IndexedDocument
from typing import List

_instance = IndexHandler()

def get_relevant_indexes(raw_query: str) -> List[IndexedDocument]:
    return _instance.get_relevant_indexes(raw_query)