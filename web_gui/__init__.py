from typing import List

from contracts.either import Either
from contracts.errors import AppError
from contracts.rich_result.rich_result import RichResult
from .web_gui import WebGUI
from shared.logger import get_logger
from contracts.use_cases import SystemRequest, SystemResponse

_gui = WebGUI()
_logger = get_logger(__name__)

def wait_request() -> SystemRequest:
    _logger.info("Waiting for user request")
    return _gui.wait_request()

def show(response: SystemResponse) -> None:
    _logger.info(f"Showing response: {type(response).__name__}")
    _gui.show(response)
