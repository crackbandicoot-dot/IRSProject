from typing import List

from Contracts.RichResult import RichResult
from .GUI import GUI

_gui = GUI()


def wait_query() -> str:
    return _gui.wait_query()


def show_result(search_results: List[RichResult]) -> None:
    _gui.show_result(search_results)
