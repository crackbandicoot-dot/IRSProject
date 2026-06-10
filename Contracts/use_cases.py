from dataclasses import dataclass
from typing import Union, List
from contracts.either import Either
from contracts.errors.unsupported_feature_exception import UnsupportedFeatureException # Just as example, but I should use AppError if possible
from contracts.errors import AppError
from contracts.rich_result.rich_result import RichResult

@dataclass
class SearchRequest:
    query: str

@dataclass
class ImproveQueryRequest:
    query: str

SystemRequest = Union[SearchRequest, ImproveQueryRequest]

@dataclass
class SearchResultsResponse:
    results: Either[AppError, List[RichResult]]

@dataclass
class RAGResponse:
    rag: Either[AppError, str]

@dataclass
class ImprovedQueryResponse:
    improved_query: Either[AppError, str]

SystemResponse = Union[SearchResultsResponse, RAGResponse, ImprovedQueryResponse]
