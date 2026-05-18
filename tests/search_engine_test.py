import pytest
from typing import Tuple, List

from Contracts.IndexedDocument import IndexedDocument
from Contracts.QueryNodes import HedgeNode, TermNode
from SearchEngine.SearchEngine import SearchEngine

@pytest.fixture
def engine_and_docs() -> Tuple[SearchEngine, List[IndexedDocument]]:
    engine = SearchEngine()
    documents = [IndexedDocument("doc-1", {"apple": 0.8})]
    return engine, documents

def test_very_hedge_intensifies_degree(engine_and_docs: Tuple[SearchEngine, List[IndexedDocument]]) -> None:
    engine, documents = engine_and_docs
    query = HedgeNode("VERY", TermNode("apple"))

    results = engine.search(documents, query)

    assert len(results) == 1
    assert results[0].score == pytest.approx(0.64, abs=1e-6)

def test_slightly_hedge_dilutes_degree(engine_and_docs: Tuple[SearchEngine, List[IndexedDocument]]) -> None:
    engine, documents = engine_and_docs
    query = HedgeNode("SLIGHTLY", TermNode("apple"))

    results = engine.search(documents, query)

    assert len(results) == 1
    assert results[0].score == pytest.approx(0.8 ** 0.5, abs=1e-6)

def test_unknown_hedge_keeps_original_degree(engine_and_docs: Tuple[SearchEngine, List[IndexedDocument]]) -> None:
    engine, documents = engine_and_docs
    query = HedgeNode("CUSTOM", TermNode("apple"))

    results = engine.search(documents, query)

    assert len(results) == 1
    assert results[0].score == pytest.approx(0.8, abs=1e-6)
