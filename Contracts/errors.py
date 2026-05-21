from typing import Union


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

class EmbeddingGenerationError(Exception):
    def __init__(self, message: str = "Failed to generate embedding from the API") -> None:
        self.message = message
        super().__init__(self.message)

class UnsupportedFeatureException(Exception):
    """Raised when a requested feature (like a specific distance metric) is not supported by the database."""
    def __init__(self, feature_name: str, message: str = "") -> None:
        self.feature_name = feature_name
        full_message = f"Unsupported feature: {feature_name}"
        if message:
            full_message += f" ({message})"
        super().__init__(full_message)

AppError = Union[QueryError, EmbeddingGenerationError, UnsupportedFeatureException]