class AlphaError(Exception):
    """Base exception for all errors in Project Alpha."""

    pass


class InfrastructureError(AlphaError):
    """Base class for all system and infrastructure failures."""

    pass


class ConfigurationError(InfrastructureError):
    """Raised when environment variables or dynamic configurations fail to load/validate."""

    pass
