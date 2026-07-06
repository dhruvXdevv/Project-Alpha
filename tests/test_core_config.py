import os
from collections.abc import Generator
from unittest import mock

import pytest
from pydantic import ValidationError as PydanticValidationError

from alpha.core.config import _clear_settings_cache, get_settings
from alpha.core.exceptions import ConfigurationError


@pytest.fixture(autouse=True)
def clear_settings_cache() -> Generator[None, None, None]:
    """Automatically reset the settings cache before and after each test."""
    _clear_settings_cache()
    yield
    _clear_settings_cache()


def test_valid_default_settings() -> None:
    """Verify default configurations load successfully when no env vars are present."""
    with mock.patch.dict(os.environ, {}, clear=True):
        settings = get_settings()
        assert settings.alpha_env == "development"
        assert settings.log_level == "INFO"
        assert settings.max_slippage_rate == 0.005
        assert settings.max_portfolio_drawdown == 0.15


def test_environment_overrides() -> None:
    """Verify environment variables take precedence when loading configurations."""
    test_env = {
        "ALPHA_ENV": "production",
        "LOG_LEVEL": "WARNING",
        "MAX_SLIPPAGE_RATE": "0.02",
        "MAX_PORTFOLIO_DRAWDOWN": "0.25",
    }
    with mock.patch.dict(os.environ, test_env, clear=True):
        settings = get_settings()
        assert settings.alpha_env == "production"
        assert settings.log_level == "WARNING"
        assert settings.max_slippage_rate == 0.02
        assert settings.max_portfolio_drawdown == 0.25


def test_research_environment() -> None:
    """Verify the research environment mode is accepted as a valid environment."""
    with mock.patch.dict(os.environ, {"ALPHA_ENV": "research"}, clear=True):
        settings = get_settings()
        assert settings.alpha_env == "research"


def test_invalid_environment() -> None:
    """Verify ConfigurationError is raised when an unsupported environment mode is supplied."""
    with mock.patch.dict(os.environ, {"ALPHA_ENV": "invalid_mode"}, clear=True):
        with pytest.raises(ConfigurationError):
            get_settings()


def test_invalid_log_level() -> None:
    """Verify ConfigurationError is raised when an unsupported log level is supplied."""
    with mock.patch.dict(os.environ, {"LOG_LEVEL": "TRACE"}, clear=True):
        with pytest.raises(ConfigurationError):
            get_settings()


def test_invalid_slippage_rate_upper_bound() -> None:
    """Verify ConfigurationError is raised when slippage rate is greater than 1.0."""
    with mock.patch.dict(os.environ, {"MAX_SLIPPAGE_RATE": "1.05"}, clear=True):
        with pytest.raises(ConfigurationError):
            get_settings()


def test_invalid_slippage_rate_lower_bound() -> None:
    """Verify ConfigurationError is raised when slippage rate is negative."""
    with mock.patch.dict(os.environ, {"MAX_SLIPPAGE_RATE": "-0.01"}, clear=True):
        with pytest.raises(ConfigurationError):
            get_settings()


def test_invalid_portfolio_drawdown_upper_bound() -> None:
    """Verify ConfigurationError is raised when drawdown is greater than 1.0."""
    with mock.patch.dict(os.environ, {"MAX_PORTFOLIO_DRAWDOWN": "1.1"}, clear=True):
        with pytest.raises(ConfigurationError):
            get_settings()


def test_invalid_portfolio_drawdown_lower_bound() -> None:
    """Verify ConfigurationError is raised when drawdown is negative."""
    with mock.patch.dict(os.environ, {"MAX_PORTFOLIO_DRAWDOWN": "-0.5"}, clear=True):
        with pytest.raises(ConfigurationError):
            get_settings()


def test_cache_behavior() -> None:
    """Verify get_settings returns the exact same instance unless cache is cleared."""
    with mock.patch.dict(os.environ, {}, clear=True):
        settings_1 = get_settings()
        settings_2 = get_settings()
        assert settings_1 is settings_2


def test_settings_immutability() -> None:
    """Verify settings object is frozen and properties cannot be modified post-initialization."""
    with mock.patch.dict(os.environ, {}, clear=True):
        settings = get_settings()
        with pytest.raises(PydanticValidationError):
            setattr(settings, "alpha_env", "production")
