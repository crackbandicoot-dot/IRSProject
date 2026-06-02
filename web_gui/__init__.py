from typing import List

from packaging.pylock import _logger
from contracts.either import Either
from contracts.errors import AppError
from contracts.rich_result import RichResult
from .web_gui import WebGUI
from shared.logger import get_logger
_gui = WebGUI()
_logger = get_logger(__name__)

def wait_query() -> str:
    _logger.info("Waiting for user query")
    return _gui.wait_query()

def show_search_results(
    search_results_either: Either[AppError, List[RichResult]]
) -> None:
    _logger.info("Tryng to show search results on UI")
    _gui.show_search_results(search_results_either)

def show_rag_results(
    rag_message_either: Either[AppError, str]
) -> None:
    _logger.info("Tryng to show rag results on UI")
    _gui.show_rag_results(rag_message_either)
