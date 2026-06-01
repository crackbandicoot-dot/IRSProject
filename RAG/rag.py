from .GitHubModelsRAG import GitHubModelsRAG
from contracts.either import Either, railway
from contracts.rich_result import RichResult
from contracts.errors import AppError
from shared.logger import get_logger
_instance = GitHubModelsRAG()
_logger = get_logger(__name__)
@railway
def process(query: str, rich_results: Either[AppError, list[RichResult]]) -> str:
    _logger.info("Tryng to make retrieval augmented generation for query")
    results = rich_results.unwrap()
    context = [r["snippet"] for r in results]
    return _instance.process(query, context)
