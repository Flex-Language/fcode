"""
Configuration package for Flex AI Agent.

This package handles all configuration management including environment variables,
settings validation, and application configuration using pydantic-settings.
"""

from .settings import (
    Settings,
    OpenRouterSettings,
    FlexSettings,
    ApplicationSettings,
    get_settings,
    validate_settings,
    load_env
)

__all__ = [
    "Settings",
    "OpenRouterSettings", 
    "FlexSettings",
    "ApplicationSettings",
    "get_settings",
    "validate_settings",
    "load_env"
]

__version__ = "1.0.0"