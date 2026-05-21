from typing import Dict
from contracts.query_nodes import TermNode


class IndexedDocument:
    def __init__(self, doc_id: str, term_weights: Dict[str, float]) -> None:
        self.id = doc_id
        self._term_weights = term_weights

    def __getitem__(self, term_node: TermNode) -> float:
        return self._term_weights.get(term_node.term, 0.0)
