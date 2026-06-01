class HandledToken(Exception):
    """An ultra-lightweight token used purely for control flow."""
    __slots__ = ()  # Saves memory by preventing __dict__ creation

    def __str__(self) -> str:
        return "HandledToken"

    