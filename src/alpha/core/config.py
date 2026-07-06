from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from alpha.core.exceptions import ConfigurationError

__all__ = ["SystemSettings", "get_settings"]


class SystemSettings(BaseSettings):
    """
    System configuration settings for Project Alpha.

    This class defines the configuration variables, their types, and validation rules.
    It is immutable (frozen) after initialization.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        frozen=True,
        extra="ignore",
    )

    alpha_env: Literal["development", "testing", "staging", "production", "research"] = Field(
        default="development",
        validation_alias="ALPHA_ENV",
    )

    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        validation_alias="LOG_LEVEL",
    )

    max_slippage_rate: float = Field(
        default=0.005,
        validation_alias="MAX_SLIPPAGE_RATE",
    )

    max_portfolio_drawdown: float = Field(
        default=0.15,
        validation_alias="MAX_PORTFOLIO_DRAWDOWN",
    )

    @field_validator("max_slippage_rate")
    @classmethod
    def validate_slippage_rate(cls, value: float) -> float:
        """Ensure slippage rate is between 0 and 1 inclusive."""
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"Slippage rate must be between 0.0 and 1.0, got {value}")
        return value

    @field_validator("max_portfolio_drawdown")
    @classmethod
    def validate_portfolio_drawdown(cls, value: float) -> float:
        """Ensure portfolio drawdown limit is between 0 and 1 inclusive."""
        if not (0.0 <= value <= 1.0):
            raise ValueError(f"Portfolio drawdown must be between 0.0 and 1.0, got {value}")
        return value


@lru_cache(maxsize=1)
def get_settings() -> SystemSettings:
    """
    Retrieve the application settings.

    This is a factory function that caches the loaded SystemSettings instance.
    If validation fails or environment variables cannot be loaded, raises ConfigurationError.
    """
    return _load_settings()


def _load_settings() -> SystemSettings:
    """
    Load and validate settings internally.

    Raises ConfigurationError if Pydantic validation fails.
    """
    try:
        return SystemSettings()
    except Exception as err:
        raise ConfigurationError(f"Failed to load system settings: {err}") from err


def _clear_settings_cache() -> None:
    """
    Clear the cached settings instance.

    This is an internal helper for use in tests only.
    External callers should never know the implementation uses lru_cache.
    If a public reset API is required in future, expose it as reset_settings_cache().
    """
    get_settings.cache_clear()
