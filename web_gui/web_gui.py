from typing import List

from contracts.either import Either, Ok, Error
from contracts.errors import AppError
from contracts.rich_result.rich_result import RichResult
from .server import WebServer

class WebGUI:
    def __init__(self, port: int = 5000) -> None:
        self._server = WebServer()
        self._server.run(port)

    def wait_query(self) -> str:
        return self._server.wait_query()

    def show_search_results(self, search_results_either: Either[AppError, List[RichResult]]) -> None:
        results_data = {}
        match search_results_either:
            case Ok(value=search_results):
                results_data["data"] = search_results
            case Error(error=app_error):
                results_data["error"] = getattr(app_error, 'error_message', str(app_error))
                
        self._server.show_search_results(results_data)

    def show_rag_results(self, rag_message_either: Either[AppError, str]) -> None:
        rag_data = {}
        match rag_message_either:
            case Ok(value=message):
                rag_data["message"] = message
            case Error(error=app_error):
                rag_data["error"] = getattr(app_error, 'error_message', str(app_error))

        self._server.show_rag_results(rag_data)
