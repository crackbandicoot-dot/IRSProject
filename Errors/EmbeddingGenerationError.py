class EmbeddingGenerationError(Exception):
    def __init__(self, message: str = "Failed to generate embedding from the API") -> None:
        self.message = message
        super().__init__(self.message)
