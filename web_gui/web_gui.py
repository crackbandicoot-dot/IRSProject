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

    def show_result(self, 
                    search_results_either: Either[AppError, List[RichResult]], 
                    rag_message_either: Either[AppError, str]) -> None:
        
        results_data = {}
        match search_results_either:
            case Ok(value=search_results):
                results_data["data"] = search_results
            case Error(error=app_error):
                results_data["error"] = getattr(app_error, 'error_message', str(app_error))
                
        rag_data = {}
        match rag_message_either:
            case Ok(value=message):
                rag_data["message"] = message
            case Error(error=app_error):
                rag_data["error"] = getattr(app_error, 'error_message', str(app_error))

        self._server.show_result(results_data, rag_data)
