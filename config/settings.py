"""
Settings configuration for Flex AI Agent.

This module provides configuration management using pydantic-settings and python_dotenv
as specified in CLAUDE.md requirements.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


def load_env() -> None:
    """Load environment variables from .env file."""
    load_dotenv()


class OpenRouterSettings(BaseModel):
    """OpenRouter API configuration."""
    
    api_key: str = Field(..., description="OpenRouter API key")
    base_url: str = Field(
        default="https://openrouter.ai/api/v1", 
        description="OpenRouter API base URL"
    )
    http_referer: str = Field(
        default="https://github.com/flex-ai-agent",
        description="HTTP Referer header for OpenRouter requests"
    )
    app_title: str = Field(
        default="Flex AI Agent",
        description="Application title for OpenRouter requests"
    )
    
    @field_validator('api_key')
    @classmethod
    def validate_api_key(cls, v):
        """Validate OpenRouter API key."""
        if not v or v.strip() == "":
            raise ValueError("OpenRouter API key cannot be empty")
        return v.strip()


class FlexSettings(BaseModel):
    """Flex programming language configuration."""
    
    cli_path: str = Field(
        default="flex", 
        description="Path to Flex CLI executable"
    )
    examples_dir: str = Field(
        default="./flex_examples",
        description="Directory for Flex code examples"
    )
    temp_dir: str = Field(
        default="./temp",
        description="Temporary directory for Flex files"
    )
    file_extensions: list[str] = Field(
        default=[".flex", ".flx"],
        description="Supported Flex file extensions"
    )


class ApplicationSettings(BaseModel):
    """General application configuration."""
    
    max_code_length: int = Field(
        default=500,
        ge=50,
        le=2000,
        description="Maximum code length per CLAUDE.md"
    )
    execution_timeout: int = Field(
        default=30,
        ge=5,
        le=300,
        description="Execution timeout in seconds"
    )
    enable_file_operations: bool = Field(
        default=True,
        description="Enable file read/write operations"
    )
    model_cache_duration: int = Field(
        default=3600,
        ge=300,
        le=86400,
        description="Model cache duration in seconds"
    )
    default_model: str = Field(
        default="anthropic/claude-3-5-sonnet",
        description="Default OpenRouter model"
    )


class Settings(BaseSettings):
    """Main application settings."""
    
    openrouter: OpenRouterSettings
    flex: FlexSettings = Field(default_factory=FlexSettings)
    app: ApplicationSettings = Field(default_factory=ApplicationSettings)
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "env_nested_delimiter": "__",
        "extra": "ignore"  # Allow extra fields in .env
    }
    
    @field_validator('openrouter', mode='before')
    @classmethod
    def validate_openrouter(cls, v):
        """Validate OpenRouter configuration."""
        if isinstance(v, dict):
            return OpenRouterSettings(**v)
        return v


def get_settings() -> Settings:
    """Get application settings with environment variables loaded."""
    load_env()
    
    # Create OpenRouter settings from environment variables
    openrouter_settings = OpenRouterSettings(
        api_key=os.getenv("OPENROUTER_API_KEY", ""),
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        http_referer=os.getenv("OPENROUTER_HTTP_REFERER", "https://github.com/flex-ai-agent"),
        app_title=os.getenv("OPENROUTER_APP_TITLE", "Flex AI Agent")
    )
    
    # Create Flex settings from environment variables  
    flex_settings = FlexSettings(
        cli_path=os.getenv("FLEX_CLI_PATH", "flex"),
        examples_dir=os.getenv("FLEX_EXAMPLES_DIR", "./flex_examples"),
        temp_dir=os.getenv("FLEX_TEMP_DIR", "./temp"),
        file_extensions=os.getenv("FLEX_FILE_EXTENSIONS", ".flex,.flx").split(",")
    )
    
    # Create application settings from environment variables
    app_settings = ApplicationSettings(
        max_code_length=int(os.getenv("MAX_CODE_LENGTH", "500")),
        execution_timeout=int(os.getenv("EXECUTION_TIMEOUT", "30")),
        enable_file_operations=os.getenv("ENABLE_FILE_OPERATIONS", "true").lower() == "true",
        model_cache_duration=int(os.getenv("MODEL_CACHE_DURATION", "3600")),
        default_model=os.getenv("DEFAULT_MODEL", "anthropic/claude-3-5-sonnet")
    )
    
    return Settings(
        openrouter=openrouter_settings,
        flex=flex_settings,
        app=app_settings
    )


def validate_settings(settings: Settings) -> None:
    """Validate required settings are present."""
    if not settings.openrouter.api_key:
        raise ValueError(
            "OpenRouter API key is required. Please set OPENROUTER_API_KEY environment variable."
        )
    
    if not settings.flex.cli_path:
        raise ValueError(
            "Flex CLI path is required. Please set FLEX_CLI_PATH environment variable."
        )


# Global settings instance
settings = get_settings()