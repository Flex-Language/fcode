"""
User Interface package for Flex AI Agent.

This package contains all user interface components including the CLI,
model selector, and output formatters for the Flex AI Agent.
"""

from .cli import FlexCLI, main
from .model_selector import ModelSelector
from .formatters import FlexFormatter, format_flex_code, format_model_info

__all__ = [
    "FlexCLI",
    "main",
    "ModelSelector",
    "FlexFormatter",
    "format_flex_code",
    "format_model_info"
]

__version__ = "1.0.0"