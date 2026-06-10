from typing import Literal
class ModelGenerationError(Exception):
    def __init__(self, message: str,provider:Literal["GitHub","Google"]) -> None:
        self.provider: Literal["GitHub","Google"]
        self.error_message = message
        super().__init__(self.error_message)
