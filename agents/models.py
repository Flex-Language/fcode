"""
Core data models for Flex AI Agent.

This module contains Pydantic models for type safety and validation across
the entire application, including OpenRouter integration and Flex code handling.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import datetime


class FlexSyntaxStyle(str, Enum):
    """Flex syntax style preference."""
    FRANCO = "franco"
    ENGLISH = "english"
    MIXED = "mixed"
    AUTO = "auto"


class FlexCodeRequest(BaseModel):
    """Request for Flex code generation."""
    
    prompt: str = Field(..., description="Description of what to generate")
    syntax_style: FlexSyntaxStyle = Field(
        default=FlexSyntaxStyle.AUTO,
        description="Preferred syntax style"
    )
    include_comments: bool = Field(
        default=True,
        description="Include explanatory comments"
    )
    max_lines: int = Field(
        default=100,
        ge=1,
        le=500,
        description="Maximum lines of code per CLAUDE.md"
    )
    model_id: Optional[str] = Field(
        None,
        description="OpenRouter model ID to use"
    )
    
    @field_validator('prompt')
    @classmethod
    def validate_prompt(cls, v):
        """Validate prompt is not empty."""
        if not v or v.strip() == "":
            raise ValueError("Prompt cannot be empty")
        return v.strip()


class FlexCodeResponse(BaseModel):
    """Response containing generated Flex code."""
    
    code: str = Field(..., description="Generated Flex code")
    syntax_style: FlexSyntaxStyle = Field(
        ...,
        description="Detected/used syntax style"
    )
    explanation: str = Field(..., description="Code explanation")
    filename: Optional[str] = Field(
        None,
        description="Suggested filename"
    )
    model_used: str = Field(..., description="Model that generated the code")
    generation_time: float = Field(
        ...,
        description="Time taken to generate in seconds"
    )
    warnings: List[str] = Field(
        default=[],
        description="Code warnings or safety notes"
    )
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        """Validate generated code is not empty."""
        if not v or v.strip() == "":
            raise ValueError("Generated code cannot be empty")
        return v.strip()


class Architecture(BaseModel):
    modality: str
    instruct_type: Optional[str] = None

class TopProvider(BaseModel):
    context_length: Optional[int] = None
    is_moderated: bool = False

class OpenRouterModel(BaseModel):
    """OpenRouter model information."""
    
    id: str = Field(..., description="Model ID")
    name: str = Field(..., description="Human-readable model name")
    description: Optional[str] = Field(
        None,
        description="Model description"
    )
    pricing: Dict[str, float] = Field(
        ...,
        description="Pricing information (prompt/completion tokens)"
    )
    context_length: int = Field(
        ...,
        description="Maximum context length"
    )
    architecture: Optional[Architecture] = Field(
        None,
        description="Model architecture"
    )
    top_provider: Optional[TopProvider] = Field(
        None,
        description="Top provider for this model"
    )
    per_request_limits: Optional[Dict[str, Any]] = Field(
        None,
        description="Per-request limits"
    )
    supports_tools: bool = Field(
        default=False,
        description="Supports function calling"
    )
    supports_streaming: bool = Field(
        default=False,
        description="Supports streaming responses"
    )
    
    @field_validator('id')
    @classmethod
    def validate_id(cls, v):
        """Validate model ID format."""
        if not v or "/" not in v:
            raise ValueError("Model ID must be in format 'provider/model'")
        return v


class ModelFilter(BaseModel):
    """Model filtering criteria."""
    
    search_term: Optional[str] = Field(
        None,
        description="Search term for name/description"
    )
    max_price_prompt: Optional[float] = Field(
        None,
        ge=0,
        description="Max price per prompt token"
    )
    max_price_completion: Optional[float] = Field(
        None,
        ge=0,
        description="Max price per completion token"
    )
    min_context_length: Optional[int] = Field(
        None,
        ge=1000,
        description="Minimum context length"
    )
    provider: Optional[str] = Field(
        None,
        description="Specific provider"
    )
    architecture: Optional[str] = Field(
        None,
        description="Model architecture"
    )
    supports_tools: Optional[bool] = Field(
        None,
        description="Supports function calling"
    )
    supports_streaming: Optional[bool] = Field(
        None,
        description="Supports streaming responses"
    )
    free_models_only: bool = Field(
        default=False,
        description="Show only free models"
    )


class ModelSelection(BaseModel):
    """Model selection result."""
    
    model: OpenRouterModel = Field(..., description="Selected model")
    reason: str = Field(..., description="Reason for selection")
    alternatives: List[OpenRouterModel] = Field(
        default=[],
        description="Alternative models"
    )
    cost_estimate: Optional[float] = Field(
        None,
        description="Estimated cost for typical usage"
    )


class FlexExecutionRequest(BaseModel):
    """Request to execute Flex code."""
    
    code: str = Field(..., description="Flex code to execute")
    filename: Optional[str] = Field(
        None,
        description="Filename for the code"
    )
    save_to_file: bool = Field(
        default=True,
        description="Whether to save code to file"
    )
    timeout: int = Field(
        default=30,
        ge=1,
        le=300,
        description="Execution timeout in seconds"
    )
    
    @field_validator('code')
    @classmethod
    def validate_code(cls, v):
        """Validate code is not empty."""
        if not v or v.strip() == "":
            raise ValueError("Code cannot be empty")
        return v.strip()


class FlexExecutionResult(BaseModel):
    """Result of Flex code execution."""
    
    success: bool = Field(..., description="Whether execution was successful")
    output: str = Field(..., description="Program output")
    error: Optional[str] = Field(
        None,
        description="Error message if failed"
    )
    execution_time: float = Field(
        ...,
        description="Execution time in seconds"
    )
    filename: Optional[str] = Field(
        None,
        description="File that was executed"
    )
    exit_code: int = Field(
        default=0,
        description="Process exit code"
    )


class FlexError(BaseModel):
    """Flex language error with context."""
    
    error_type: str = Field(..., description="Type of error")
    message: str = Field(..., description="Error message")
    line_number: Optional[int] = Field(
        None,
        description="Line number if applicable"
    )
    column_number: Optional[int] = Field(
        None,
        description="Column number if applicable"
    )
    suggestion: str = Field(..., description="Suggested fix")
    prevention: str = Field(..., description="How to prevent this error")
    is_franco_loop_error: bool = Field(
        default=False,
        description="Whether this is a Franco l7d loop safety error"
    )


class CodeValidationResult(BaseModel):
    """Result of Flex code validation."""
    
    is_valid: bool = Field(..., description="Whether code is valid")
    syntax_style: FlexSyntaxStyle = Field(
        ...,
        description="Detected syntax style"
    )
    errors: List[FlexError] = Field(
        default=[],
        description="Validation errors"
    )
    warnings: List[str] = Field(
        default=[],
        description="Validation warnings"
    )
    suggestions: List[str] = Field(
        default=[],
        description="Improvement suggestions"
    )
    has_franco_loop_safety_issues: bool = Field(
        default=False,
        description="Whether Franco l7d loop safety issues were found"
    )


class AgentSession(BaseModel):
    """Agent conversation session."""
    
    session_id: str = Field(..., description="Unique session identifier")
    current_model: str = Field(..., description="Currently selected model")
    conversation_history: List[Dict[str, Any]] = Field(
        default=[],
        description="Conversation history"
    )
    user_preferences: Dict[str, Any] = Field(
        default={},
        description="User preferences and settings"
    )
    created_at: datetime = Field(
        default_factory=datetime.now,
        description="Session creation timestamp"
    )
    last_activity: datetime = Field(
        default_factory=datetime.now,
        description="Last activity timestamp"
    )


class ModelMetrics(BaseModel):
    """Model performance metrics."""
    
    model_id: str = Field(..., description="Model identifier")
    total_requests: int = Field(
        default=0,
        description="Total requests made"
    )
    successful_requests: int = Field(
        default=0,
        description="Successful requests"
    )
    failed_requests: int = Field(
        default=0,
        description="Failed requests"
    )
    average_response_time: float = Field(
        default=0.0,
        description="Average response time in seconds"
    )
    total_tokens_used: int = Field(
        default=0,
        description="Total tokens consumed"
    )
    total_cost: float = Field(
        default=0.0,
        description="Total cost in USD"
    )
    last_used: Optional[datetime] = Field(
        None,
        description="Last usage timestamp"
    )


class FileOperation(BaseModel):
    """File operation request."""
    
    operation: str = Field(..., description="Operation type (read/write/delete)")
    filepath: str = Field(..., description="File path")
    content: Optional[str] = Field(
        None,
        description="File content for write operations"
    )
    encoding: str = Field(
        default="utf-8",
        description="File encoding"
    )
    backup: bool = Field(
        default=True,
        description="Create backup before write/delete"
    )
    
    @field_validator('operation')
    @classmethod
    def validate_operation(cls, v):
        """Validate operation type."""
        valid_operations = ['read', 'write', 'delete', 'exists', 'list']
        if v not in valid_operations:
            raise ValueError(f"Operation must be one of: {valid_operations}")
        return v


class FileOperationResult(BaseModel):
    """Result of file operation."""
    
    success: bool = Field(..., description="Whether operation succeeded")
    message: str = Field(..., description="Operation message")
    content: Optional[str] = Field(
        None,
        description="File content for read operations"
    )
    filepath: str = Field(..., description="File path")
    backup_path: Optional[str] = Field(
        None,
        description="Backup file path if created"
    )
    file_size: Optional[int] = Field(
        None,
        description="File size in bytes"
    )
    last_modified: Optional[datetime] = Field(
        None,
        description="Last modification timestamp"
    )