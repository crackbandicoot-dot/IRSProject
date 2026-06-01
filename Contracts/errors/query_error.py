class QueryError(Exception):
    def __init__(self, error_location: int, error_message: str) -> None:
        self._error_location = error_location
        self._error_message = error_message
        super().__init__(f"On word {error_location}: {error_message}")

    @property
    def error_location(self) -> int:
        return self._error_location

    @property
    def error_message(self) -> str:
        return self._error_message