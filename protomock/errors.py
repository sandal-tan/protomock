"""Protomock errors."""

class NoMockFoundError(Exception):
    """Exception to raise when no mock has been registered."""

class NoProviderError(Exception):
    """Exception to raise when a provider cannot be found."""
