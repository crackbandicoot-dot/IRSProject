from contracts.use_cases import SystemRequest, SystemResponse
from .server import WebServer

class WebGUI:
    def __init__(self, port: int = 5000) -> None:
        self._server = WebServer()
        self._server.run(port)

    def wait_request(self) -> SystemRequest:
        return self._server.wait_request()

    def show(self, response: SystemResponse) -> None:
        self._server.show(response)
