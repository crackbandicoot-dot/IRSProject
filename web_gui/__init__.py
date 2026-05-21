from typing import List
from contracts.either import Either
from contracts.errors import AppError
from contracts.rich_result.rich_result import RichResult
from .web_gui import WebGUI

_gui = WebGUI()

def wait_query() -> str:
    return _gui.wait_query()

def show_result(
    search_results_either: Either[AppError, List[RichResult]], 
    rag_message_either: Either[AppError, str]
) -> None:
    _gui.show_result(search_results_either, rag_message_either)
