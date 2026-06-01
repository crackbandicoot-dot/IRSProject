class UnsupportedFeatureException(Exception):
    """Raised when a requested feature (like a specific distance metric) is not supported by the database."""
    def __init__(self, feature_name: str, message: str = "") -> None:
        self.feature_name = feature_name
        full_message = f"Unsupported feature: {feature_name}"
        if message:
            full_message += f" ({message})"
        super().__init__(full_message)