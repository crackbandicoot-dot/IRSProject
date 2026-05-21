import os
import pytest
from rag.rag import process


def test_rag_process_integration() -> None:
    query = "What is the capital of France?"
    context = ["Paris is the capital of France.", "France is a country in Europe."]
    result = process(query, context)
    
    assert result is not None
    assert type(result) is str
    assert "Paris" in result
