from typing import TypedDict


class RichResult(TypedDict):
    title: str
    snippet: str
    score: float
    url:str

class RAGResult(TypedDict):
    title: str
    content: str
    url: str
