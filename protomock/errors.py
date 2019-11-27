"""Protomock errors."""

class NoMockFoundError(Exception):
    """Exception to raise when no mock has been registered."""

class NoProviderError(Exception):
    """Exception to raise when a provider cannot be found."""

class UnknownFieldError(Exception):
    """Exception to raise when an unknown field is requested from a Message."""

    def __init__(self, field_name: str, message_name: str):
        super().__init__(f'Unknown field {field_name} for Message {message_name}')
