name: "AI Agent for Flex Programming Language with OpenRouter Integration"
description: |

## Purpose
Build a comprehensive AI agent that understands and generates code for the Flex programming language with full OpenRouter.ai integration, allowing users to select from 400+ AI models. The agent leverages the extensive language specification in `data/flex_language_spec.json` and provides intelligent code generation, error handling, and interactive CLI support with both Franco Arabic and English syntax patterns.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats from the Flex language spec
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the Flex specification
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Create a production-ready AI agent that can understand, generate, and execute Flex programming language code with full OpenRouter integration for model selection, complete with CLI interface, file operations, and intelligent error handling across 400+ AI models.

## Why
- **Business value**: Democratizes Flex programming by providing an intelligent assistant with model choice
- **Integration**: Bridges cultural and linguistic gaps with dual-syntax support
- **Model flexibility**: Allows users to choose optimal models for different tasks
- **Problems this solves**: 
  - Reduces learning curve for Flex programming
  - Prevents common syntax errors (especially Franco l7d loop safety)
  - Provides contextual help and code generation across multiple AI models
  - Enables rapid prototyping and development with model optimization
  - Offers cost-effective model selection based on task complexity

## What
A CLI-based AI agent that:
- Generates Flex source files with proper syntax (Franco or English)
- Executes Flex files via CLI (`flex {filename}`)
- Provides intelligent code suggestions and error explanations
- Integrates with OpenRouter.ai for access to 400+ AI models
- Supports model listing, searching, and filtering
- Allows dynamic model selection based on task requirements
- Reads and writes files from the filesystem
- Supports interactive conversations with context memory
- Validates code against Flex language specification

### Success Criteria
- [ ] Agent successfully generates valid Flex code in both Franco and English syntax
- [ ] Agent can execute generated Flex files via CLI
- [ ] Agent provides accurate error explanations and fixes
- [ ] Agent follows Flex best practices (no semicolons, safe loop bounds, etc.)
- [ ] OpenRouter integration allows model listing and selection
- [ ] Model filtering by cost, capability, and provider works correctly
- [ ] CLI interface is intuitive and responsive with model selection features
- [ ] All unit tests pass with 80%+ coverage
- [ ] Code follows project conventions from CLAUDE.md

## All Needed Context

### Documentation & References
```yaml
# MUST READ - Include these in your context window
- file: /Users/mikawi/Developer/grad/flex_code/data/flex_language_spec.json
  why: Complete Flex language specification - syntax, patterns, error handling, best practices
  critical: Contains ai_system_prompt with safety rules for Franco l7d loops
  
- url: https://ai.pydantic.dev/agents/
  why: Core PydanticAI agent creation patterns and architecture
  
- url: https://ai.pydantic.dev/models/
  why: PydanticAI model provider patterns and configuration
  
- url: https://openrouter.ai/docs/community/pydantic-ai
  why: PydanticAI OpenRouter integration documentation
  
- url: https://openrouter.ai/docs/api-reference/list-available-models
  why: OpenRouter models API for listing and filtering
  
- url: https://openrouter.ai/docs/api-reference/authentication
  why: OpenRouter API authentication patterns
  
- url: https://openrouter.ai/docs/features/model-routing
  why: OpenRouter model routing and fallback patterns
  
- url: https://github.com/OpenRouterTeam/openrouter-examples-python
  why: Official OpenRouter Python integration examples
  
- file: /Users/mikawi/Developer/grad/flex_code/PRPs/EXAMPLE_multi_agent_prp.md
  why: Example PRP structure and implementation patterns to follow
  
- file: /Users/mikawi/Developer/grad/flex_code/CLAUDE.md
  why: Project-specific rules, conventions, and requirements
  
- file: /Users/mikawi/Developer/grad/flex_code/codefetch/codebase.md
  why: Project structure, conventions, and meta-guidelines
```

### Current Codebase tree
```bash
.
├── CLAUDE.md
├── codefetch/
│   └── codebase.md
├── data/
│   └── flex_language_spec.json
├── examples/
├── INITIAL_EXAMPLE.md
├── INITIAL.md
├── LICENSE
├── PRPs/
│   ├── EXAMPLE_multi_agent_prp.md
│   ├── flex_ai_agent.md
│   └── templates/
│       └── prp_base.md
└── README.md
```

### Desired Codebase tree with files to be added and responsibility of file
```bash
.
├── agents/
│   ├── __init__.py               # Package initialization
│   ├── flex_agent.py            # Main Flex AI agent with PydanticAI
│   ├── models.py                # Pydantic models for data validation
│   └── providers.py             # OpenRouter provider configuration
├── tools/
│   ├── __init__.py              # Package initialization
│   ├── flex_executor.py         # Flex CLI execution tool
│   ├── file_manager.py          # File read/write operations
│   ├── code_validator.py        # Flex code validation against spec
│   └── model_manager.py         # OpenRouter model management
├── config/
│   ├── __init__.py              # Package initialization
│   └── settings.py              # Environment and configuration management
├── ui/
│   ├── __init__.py              # Package initialization
│   ├── cli.py                   # Main CLI interface
│   ├── model_selector.py        # Interactive model selection interface
│   └── formatters.py            # Output formatting utilities
├── tests/
│   ├── __init__.py              # Package initialization
│   ├── test_flex_agent.py       # Main agent tests
│   ├── test_flex_executor.py    # Executor tool tests
│   ├── test_file_manager.py     # File operations tests
│   ├── test_code_validator.py   # Code validation tests
│   ├── test_model_manager.py    # Model management tests
│   ├── test_model_selector.py   # Model selection UI tests
│   └── test_cli.py              # CLI interface tests
├── main.py                      # Entry point script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── flex_examples/               # Generated Flex code examples
│   ├── franco_examples/         # Franco Arabic syntax examples
│   └── english_examples/        # English syntax examples
├── cache/                       # Model metadata cache
│   └── models_cache.json        # Cached model information
└── README.md                    # Comprehensive project documentation
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: Flex Franco l7d loops are INCLUSIVE - must use 'length(array) - 1' for bounds
# Example: karr l7d length(myList) - 1 { } to avoid out-of-bounds errors
# CRITICAL: PydanticAI requires async throughout - no sync functions in async context
# CRITICAL: OpenRouter API requires Bearer token authentication
# CRITICAL: OpenRouter rate limits vary by model - implement proper error handling
# CRITICAL: Model fallback patterns must be implemented for reliability
# CRITICAL: Use python_dotenv and load_env() for environment variables per CLAUDE.md
# CRITICAL: Never create files longer than 500 lines per CLAUDE.md
# CRITICAL: Always create Pytest unit tests for new features per CLAUDE.md
# CRITICAL: Use relative imports within packages per CLAUDE.md
# CRITICAL: Follow PEP8, use type hints, and format with black per CLAUDE.md
# CRITICAL: Use pydantic for data validation per CLAUDE.md
# CRITICAL: Write docstrings for every function using Google style per CLAUDE.md
# CRITICAL: Flex has mixed syntax support - detect user preference and match their style
# CRITICAL: Use venv_linux virtual environment for Python execution per CLAUDE.md
# CRITICAL: OpenRouter models have different parameter support - validate before use
# CRITICAL: Cache model metadata to avoid excessive API calls
# CRITICAL: Handle OpenRouter model routing and provider fallbacks gracefully
```

## Implementation Blueprint

### Data models and structure

Create the core data models to ensure type safety and consistency.
```python
# models.py - Core data structures
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
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
    syntax_style: FlexSyntaxStyle = Field(FlexSyntaxStyle.AUTO)
    include_comments: bool = Field(True)
    max_lines: int = Field(100, ge=1, le=500)
    model_id: Optional[str] = Field(None, description="OpenRouter model ID")

class FlexCodeResponse(BaseModel):
    """Response containing generated Flex code."""
    code: str = Field(..., description="Generated Flex code")
    syntax_style: FlexSyntaxStyle = Field(..., description="Detected/used syntax style")
    explanation: str = Field(..., description="Code explanation")
    filename: Optional[str] = Field(None, description="Suggested filename")
    model_used: str = Field(..., description="Model that generated the code")
    generation_time: float = Field(..., description="Time taken to generate")

class OpenRouterModel(BaseModel):
    """OpenRouter model information."""
    id: str = Field(..., description="Model ID")
    name: str = Field(..., description="Human-readable model name")
    description: Optional[str] = Field(None, description="Model description")
    pricing: Dict[str, float] = Field(..., description="Pricing information")
    context_length: int = Field(..., description="Maximum context length")
    architecture: Optional[str] = Field(None, description="Model architecture")
    top_provider: Optional[str] = Field(None, description="Top provider")
    per_request_limits: Optional[Dict[str, Any]] = Field(None, description="Request limits")

class ModelFilter(BaseModel):
    """Model filtering criteria."""
    search_term: Optional[str] = Field(None, description="Search term for name/description")
    max_price_prompt: Optional[float] = Field(None, description="Max price per prompt token")
    max_price_completion: Optional[float] = Field(None, description="Max price per completion token")
    min_context_length: Optional[int] = Field(None, description="Minimum context length")
    provider: Optional[str] = Field(None, description="Specific provider")
    architecture: Optional[str] = Field(None, description="Model architecture")
    supports_tools: Optional[bool] = Field(None, description="Supports function calling")
    free_models_only: bool = Field(False, description="Show only free models")

class ModelSelection(BaseModel):
    """Model selection result."""
    model: OpenRouterModel = Field(..., description="Selected model")
    reason: str = Field(..., description="Reason for selection")
    alternatives: List[OpenRouterModel] = Field(default=[], description="Alternative models")

class FlexExecutionRequest(BaseModel):
    """Request to execute Flex code."""
    code: str = Field(..., description="Flex code to execute")
    filename: Optional[str] = Field(None, description="Filename for the code")
    save_to_file: bool = Field(True, description="Whether to save code to file")

class FlexExecutionResult(BaseModel):
    """Result of Flex code execution."""
    success: bool = Field(..., description="Whether execution was successful")
    output: str = Field(..., description="Program output")
    error: Optional[str] = Field(None, description="Error message if failed")
    execution_time: float = Field(..., description="Execution time in seconds")
    filename: Optional[str] = Field(None, description="File that was executed")

class FlexError(BaseModel):
    """Flex language error with context."""
    error_type: str = Field(..., description="Type of error")
    message: str = Field(..., description="Error message")
    line_number: Optional[int] = Field(None, description="Line number if applicable")
    suggestion: str = Field(..., description="Suggested fix")
    prevention: str = Field(..., description="How to prevent this error")
```

### List of tasks to be completed to fulfill the PRP in the order they should be completed

```yaml
Task 1: Setup Project Structure and Configuration
CREATE config/settings.py:
  - PATTERN: Use pydantic-settings and python_dotenv per CLAUDE.md
  - Load environment variables with defaults
  - Include OpenRouter API key configuration
  - Validate required configuration

CREATE .env.example:
  - Include all required environment variables
  - Add descriptions for each variable
  - Include OpenRouter API key template
  - Follow CLAUDE.md conventions

Task 2: Create Core Data Models  
CREATE agents/models.py:
  - PATTERN: Use pydantic for data validation per CLAUDE.md
  - Define all request/response models
  - Include OpenRouter model representations
  - Include proper type hints and validation

Task 3: Implement OpenRouter Model Manager
CREATE tools/model_manager.py:
  - PATTERN: Async functions for API operations
  - Implement model listing with caching
  - Add model filtering and searching
  - Handle OpenRouter API authentication
  - Implement error handling and retries

Task 4: Create OpenRouter Provider Configuration
CREATE agents/providers.py:
  - PATTERN: Follow PydanticAI provider patterns
  - Configure OpenRouter integration
  - Support dynamic model selection
  - Handle authentication and base URL setup

Task 5: Implement Interactive Model Selection UI
CREATE ui/model_selector.py:
  - PATTERN: Use inquirer library for interactive selection
  - Implement model browsing and filtering
  - Add search functionality
  - Support model comparison and details view

Task 6: Create File Management Tool
CREATE tools/file_manager.py:
  - PATTERN: Async functions for file operations
  - Handle file reading, writing, and validation
  - Support for both .flex and .flx extensions
  - Implement secure file operations

Task 7: Implement Flex Code Validator
CREATE tools/code_validator.py:
  - PATTERN: Use flex_language_spec.json as validation source
  - Validate syntax patterns (Franco vs English)
  - Check for common errors (l7d loop safety)
  - Support batch validation

Task 8: Implement Flex Executor Tool
CREATE tools/flex_executor.py:
  - PATTERN: Async subprocess execution
  - Handle CLI command: flex {filename}
  - Capture output and errors with proper error handling
  - Support timeout and resource management

Task 9: Create Main Flex Agent
CREATE agents/flex_agent.py:
  - PATTERN: Follow PydanticAI agent creation patterns
  - Load flex_language_spec.json for system prompt
  - Register all tools (@agent.tool decorators)
  - Implement syntax detection and adaptation
  - Support dynamic model switching

Task 10: Implement CLI Interface
CREATE ui/cli.py:
  - PATTERN: Interactive CLI with streaming responses
  - Support conversation history and context
  - Integrate model selection interface
  - Color-coded output for different message types
  - Handle async properly with asyncio.run()

CREATE main.py:
  - PATTERN: Entry point with command dispatch
  - Support various CLI commands
  - Handle model selection commands
  - Implement help and documentation

Task 11: Add Output Formatting
CREATE ui/formatters.py:
  - PATTERN: Structured output formatting
  - Support code highlighting
  - Format model information displays
  - Handle error message formatting

Task 12: Add Comprehensive Tests
CREATE tests/:
  - PATTERN: Mirror project structure in tests
  - Test all major functionality with mocks
  - Include edge cases and error scenarios
  - Test OpenRouter integration thoroughly
  - Achieve 80%+ test coverage

Task 13: Create Documentation and Examples
CREATE README.md:
  - PATTERN: Follow project documentation standards
  - Include setup, installation, and usage instructions
  - Document OpenRouter integration setup
  - Provide example interactions and use cases

CREATE flex_examples/:
  - Generate example Flex programs in both syntax styles
  - Include common patterns and best practices
  - Demonstrate error handling and validation
```

### Per task pseudocode as needed added to each task

```python
# Task 3: OpenRouter Model Manager Implementation
import httpx
import json
from typing import List, Optional
from datetime import datetime, timedelta

class ModelManager:
    def __init__(self, api_key: str, cache_duration: int = 3600):
        self.api_key = api_key
        self.base_url = "https://openrouter.ai/api/v1"
        self.cache_file = "cache/models_cache.json"
        self.cache_duration = timedelta(seconds=cache_duration)
        
    async def list_models(self, use_cache: bool = True) -> List[OpenRouterModel]:
        """List all available OpenRouter models."""
        # PATTERN: Check cache first
        if use_cache and self._is_cache_valid():
            return self._load_from_cache()
        
        # PATTERN: Fetch from API with proper error handling
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/models",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "HTTP-Referer": "https://github.com/your-repo",
                        "X-Title": "Flex AI Agent"
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                # PATTERN: Parse and validate with Pydantic
                models = [OpenRouterModel(**model) for model in data.get("data", [])]
                
                # PATTERN: Cache results
                self._save_to_cache(models)
                return models
                
            except httpx.HTTPError as e:
                raise ModelManagerError(f"Failed to fetch models: {e}")
    
    async def filter_models(self, filters: ModelFilter) -> List[OpenRouterModel]:
        """Filter models based on criteria."""
        models = await self.list_models()
        filtered = []
        
        for model in models:
            if self._matches_filter(model, filters):
                filtered.append(model)
        
        return filtered
    
    def _matches_filter(self, model: OpenRouterModel, filters: ModelFilter) -> bool:
        """Check if model matches filter criteria."""
        # PATTERN: Implement comprehensive filtering logic
        if filters.search_term:
            search_lower = filters.search_term.lower()
            if not (search_lower in model.name.lower() or 
                   (model.description and search_lower in model.description.lower())):
                return False
        
        if filters.max_price_prompt:
            if model.pricing.get("prompt", float('inf')) > filters.max_price_prompt:
                return False
        
        if filters.min_context_length:
            if model.context_length < filters.min_context_length:
                return False
        
        if filters.free_models_only:
            if model.pricing.get("prompt", 0) > 0 or model.pricing.get("completion", 0) > 0:
                return False
        
        return True

# Task 9: Main Flex Agent Implementation
from pydantic_ai import Agent, RunContext
from typing import Any, Dict
import json

class FlexAgent:
    def __init__(self, model_manager: ModelManager, default_model: str = "anthropic/claude-3-5-sonnet"):
        self.model_manager = model_manager
        self.current_model = default_model
        self.conversation_history = []
        
        # Load Flex language specification
        with open('data/flex_language_spec.json', 'r') as f:
            self.flex_spec = json.load(f)
        
        # Create agent with dynamic model selection
        self.agent = self._create_agent()
    
    def _create_agent(self) -> Agent:
        """Create PydanticAI agent with OpenRouter integration."""
        return Agent(
            f"openrouter:{self.current_model}",
            system_prompt=self.flex_spec['ai_system_prompt']['description'],
            deps_type=AgentDependencies,
            result_type=FlexCodeResponse
        )
    
    async def switch_model(self, model_id: str) -> None:
        """Switch to a different model."""
        # PATTERN: Validate model exists
        models = await self.model_manager.list_models()
        if not any(m.id == model_id for m in models):
            raise ValueError(f"Model {model_id} not found")
        
        self.current_model = model_id
        self.agent = self._create_agent()
    
    @property
    def tools(self):
        """Register all agent tools."""
        return [
            self.generate_flex_code,
            self.execute_flex_code,
            self.validate_flex_code,
            self.list_available_models,
            self.switch_model_tool
        ]
    
    async def generate_flex_code(
        self, 
        ctx: RunContext[AgentDependencies],
        request: FlexCodeRequest
    ) -> FlexCodeResponse:
        """Generate Flex code based on user request."""
        # PATTERN: Analyze request and determine syntax style
        syntax_style = self._detect_syntax_preference(request.prompt, request.syntax_style)
        
        # PATTERN: Use flex_language_spec for code generation
        start_time = time.time()
        
        # PATTERN: Generate code with current model
        response = await self.agent.run(
            f"Generate Flex code for: {request.prompt}",
            deps=AgentDependencies(
                syntax_style=syntax_style,
                spec=self.flex_spec,
                max_lines=request.max_lines
            )
        )
        
        # CRITICAL: Validate generated code against spec
        validation_result = await self._validate_code(response.data)
        if not validation_result.is_valid:
            raise ValidationError(validation_result.errors)
        
        return FlexCodeResponse(
            code=response.data,
            syntax_style=syntax_style,
            explanation=self._generate_explanation(response.data, syntax_style),
            filename=self._suggest_filename(request.prompt),
            model_used=self.current_model,
            generation_time=time.time() - start_time
        )

# Task 10: CLI Interface Implementation with Model Selection
import asyncio
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
import inquirer

class FlexCLI:
    def __init__(self):
        self.console = Console()
        self.model_manager = ModelManager(os.getenv("OPENROUTER_API_KEY"))
        self.agent = FlexAgent(self.model_manager)
        self.current_session = []
    
    async def run(self):
        """Main CLI loop."""
        self.console.print("🚀 Flex AI Agent - Interactive Programming Assistant", style="bold green")
        self.console.print("Type 'help' for commands, 'models' for model selection, 'exit' to quit\n")
        
        # Show current model
        self.console.print(f"Current model: {self.agent.current_model}", style="blue")
        
        while True:
            try:
                user_input = Prompt.ask("You").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    break
                elif user_input.lower() == 'help':
                    self._show_help()
                elif user_input.lower() == 'models':
                    await self._model_selection_menu()
                elif user_input.lower().startswith('switch '):
                    model_id = user_input[7:]
                    await self._switch_model(model_id)
                else:
                    await self._process_request(user_input)
                    
            except KeyboardInterrupt:
                self.console.print("\n👋 Goodbye!", style="yellow")
                break
            except Exception as e:
                self.console.print(f"❌ Error: {e}", style="red")
    
    async def _model_selection_menu(self):
        """Interactive model selection menu."""
        self.console.print("📋 Loading available models...", style="yellow")
        
        try:
            models = await self.model_manager.list_models()
            
            # PATTERN: Create interactive selection
            choices = []
            for model in models[:50]:  # Limit to top 50 for usability
                price_info = f"${model.pricing.get('prompt', 0):.6f}/prompt"
                choice = f"{model.name} - {price_info} - {model.context_length}k ctx"
                choices.append((choice, model.id))
            
            questions = [
                inquirer.List(
                    'model',
                    message="Select a model (↑/↓ to navigate, Enter to select)",
                    choices=choices,
                    carousel=True
                )
            ]
            
            answers = inquirer.prompt(questions)
            if answers:
                await self._switch_model(answers['model'])
                
        except Exception as e:
            self.console.print(f"❌ Failed to load models: {e}", style="red")
    
    async def _switch_model(self, model_id: str):
        """Switch to a different model."""
        try:
            await self.agent.switch_model(model_id)
            self.console.print(f"✅ Switched to model: {model_id}", style="green")
        except Exception as e:
            self.console.print(f"❌ Failed to switch model: {e}", style="red")
    
    async def _process_request(self, user_input: str):
        """Process user request with streaming response."""
        self.console.print("🤖 Assistant:", style="cyan", end=" ")
        
        try:
            # PATTERN: Stream response with tool visibility
            async for chunk in self.agent.run_stream(
                user_input,
                deps=AgentDependencies(history=self.current_session)
            ):
                if chunk.kind == 'response':
                    self.console.print(chunk.content, end='')
                elif chunk.kind == 'tool-call':
                    self.console.print(f"\n🛠 Using tool: {chunk.tool_name}", style="yellow")
                    
            self.current_session.append((user_input, chunk.content))
            self.console.print()  # New line
            
        except Exception as e:
            self.console.print(f"❌ Error processing request: {e}", style="red")
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      # OpenRouter Configuration
      OPENROUTER_API_KEY=your_openrouter_api_key_here
      OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
      
      # Flex Configuration
      FLEX_CLI_PATH=flex
      FLEX_EXAMPLES_DIR=./flex_examples
      FLEX_TEMP_DIR=./temp
      
      # Application Settings
      MAX_CODE_LENGTH=500
      EXECUTION_TIMEOUT=30
      ENABLE_FILE_OPERATIONS=true
      MODEL_CACHE_DURATION=3600
      DEFAULT_MODEL=anthropic/claude-3-5-sonnet

DEPENDENCIES:
  - Update requirements.txt with:
    - pydantic-ai
    - pydantic-settings
    - python-dotenv
    - httpx
    - inquirer
    - rich
    - pytest
    - pytest-asyncio
    - pytest-cov
    - black
    - ruff
    - mypy

OPENROUTER_SETUP:
  - Create API key at https://openrouter.ai/keys
  - Set credit limits for cost control
  - Configure HTTP-Referer header for app visibility
  - Test with basic model listing call

FLEX_CLI:
  - Ensure flex CLI is installed and accessible
  - Test with: flex --version
  - Document installation instructions in README
```

## Validation Loop

### Level 1: Syntax & Style
```bash
# Run these FIRST - fix any errors before proceeding
ruff check . --fix              # Auto-fix style issues
black .                         # Format code
mypy .                          # Type checking

# Expected: No errors. If errors, READ and fix.
```

### Level 2: Unit Tests
```python
# test_model_manager.py
async def test_list_models():
    """Test OpenRouter model listing."""
    manager = ModelManager(api_key="test_key")
    
    # Mock OpenRouter API response
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": [
                {
                    "id": "anthropic/claude-3-5-sonnet",
                    "name": "Claude 3.5 Sonnet",
                    "pricing": {"prompt": 0.000015, "completion": 0.000075},
                    "context_length": 200000
                }
            ]
        }
        mock_get.return_value.__aenter__.return_value = mock_response
        
        models = await manager.list_models(use_cache=False)
        assert len(models) == 1
        assert models[0].id == "anthropic/claude-3-5-sonnet"

async def test_filter_models():
    """Test model filtering."""
    manager = ModelManager(api_key="test_key")
    filters = ModelFilter(
        max_price_prompt=0.00002,
        min_context_length=100000
    )
    
    # Test filtering logic
    models = await manager.filter_models(filters)
    for model in models:
        assert model.pricing.get("prompt", 0) <= 0.00002
        assert model.context_length >= 100000

# test_flex_agent.py
async def test_model_switching():
    """Test dynamic model switching."""
    manager = ModelManager(api_key="test_key")
    agent = FlexAgent(manager)
    
    original_model = agent.current_model
    await agent.switch_model("anthropic/claude-3-opus")
    assert agent.current_model == "anthropic/claude-3-opus"
    assert agent.current_model != original_model

async def test_flex_code_generation():
    """Test Flex code generation with OpenRouter."""
    manager = ModelManager(api_key="test_key")
    agent = FlexAgent(manager)
    
    request = FlexCodeRequest(
        prompt="create a loop that prints numbers 1 to 10",
        syntax_style=FlexSyntaxStyle.FRANCO
    )
    
    # Mock agent response
    with patch.object(agent.agent, 'run') as mock_run:
        mock_run.return_value = Mock(data='karr l7d 10 { etb3(i) }')
        
        result = await agent.generate_flex_code(None, request)
        assert result.syntax_style == FlexSyntaxStyle.FRANCO
        assert "karr l7d" in result.code
        assert result.model_used == agent.current_model

# test_cli.py
async def test_model_selection_menu():
    """Test CLI model selection interface."""
    cli = FlexCLI()
    
    # Mock inquirer prompt
    with patch('inquirer.prompt') as mock_prompt:
        mock_prompt.return_value = {'model': 'anthropic/claude-3-5-sonnet'}
        
        with patch.object(cli, '_switch_model') as mock_switch:
            await cli._model_selection_menu()
            mock_switch.assert_called_once_with('anthropic/claude-3-5-sonnet')

def test_model_filter_validation():
    """Test model filter validation."""
    # Valid filter
    filter_valid = ModelFilter(
        max_price_prompt=0.00001,
        min_context_length=50000,
        free_models_only=True
    )
    assert filter_valid.max_price_prompt == 0.00001
    
    # Invalid filter should raise validation error
    with pytest.raises(ValidationError):
        ModelFilter(min_context_length=-1)
```

```bash
# Run tests iteratively until passing:
pytest tests/ -v --cov=agents --cov=tools --cov=ui --cov-report=term-missing

# If failing: Debug specific test, fix code, re-run
```

### Level 3: Integration Test
```bash
# Test CLI interaction with model selection
python main.py

# Expected interaction:
# 🚀 Flex AI Agent - Interactive Programming Assistant
# Type 'help' for commands, 'models' for model selection, 'exit' to quit
# 
# Current model: anthropic/claude-3-5-sonnet
# 
# You: models
# 📋 Loading available models...
# [Interactive model selection menu appears]
# 
# You: Create a simple hello world program in Franco syntax
# 🤖 Assistant: I'll create a simple hello world program using Franco Arabic syntax.
# 🛠 Using tool: generate_flex_code
# 
# Here's your Flex program:
# ```flex
# etb3("Ahlan wa sahlan - Hello World!")
# ```
# 
# Generated with: anthropic/claude-3-5-sonnet
# Time: 1.2s
# 
# You: switch anthropic/claude-3-opus
# ✅ Switched to model: anthropic/claude-3-opus
# 
# You: Now execute it
# 🤖 Assistant: I'll execute the Flex program for you.
# 🛠 Using tool: execute_flex_code
# 
# ✅ Execution successful!
# Output: Ahlan wa sahlan - Hello World!

# Test OpenRouter API integration
curl -H "Authorization: Bearer $OPENROUTER_API_KEY" \
     -H "HTTP-Referer: https://github.com/your-repo" \
     -H "X-Title: Flex AI Agent Test" \
     https://openrouter.ai/api/v1/models

# Expected: JSON response with model list
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v --cov=agents --cov=tools --cov=ui --cov-report=term-missing`
- [ ] No linting errors: `ruff check .`
- [ ] No type errors: `mypy .`
- [ ] No formatting issues: `black --check .`
- [ ] OpenRouter API integration works correctly
- [ ] Model listing and filtering functions properly
- [ ] Interactive model selection interface is responsive
- [ ] Agent generates valid Franco syntax
- [ ] Agent generates valid English syntax
- [ ] Agent detects syntax preference correctly
- [ ] Dynamic model switching works seamlessly
- [ ] Flex CLI execution works properly
- [ ] Error handling and validation work correctly
- [ ] CLI interface is responsive and user-friendly
- [ ] File operations work securely
- [ ] Franco l7d loop safety is enforced
- [ ] Model caching reduces API calls
- [ ] Cost tracking and optimization features work
- [ ] README includes comprehensive setup instructions
- [ ] All environment variables documented in .env.example

---

## Anti-Patterns to Avoid
- ❌ Don't ignore Franco l7d loop safety - this is critical
- ❌ Don't use sync functions in async agent context
- ❌ Don't hardcode OpenRouter API keys - use environment variables
- ❌ Don't skip model validation - verify models exist before switching
- ❌ Don't ignore rate limits - implement proper backoff strategies
- ❌ Don't cache models indefinitely - implement cache expiration
- ❌ Don't create files longer than 500 lines per CLAUDE.md
- ❌ Don't forget to create unit tests for new features
- ❌ Don't ignore type hints - use them consistently
- ❌ Don't commit sensitive information like API keys
- ❌ Don't assume models support all features - validate capabilities
- ❌ Don't skip error handling for network requests
- ❌ Don't make excessive API calls - implement intelligent caching
- ❌ Don't mix syntax styles incorrectly - validate combinations

## Confidence Score: 8/10

High confidence due to:
- Complete Flex language specification available with AI system prompt
- Comprehensive OpenRouter documentation and examples
- Clear PydanticAI integration patterns
- Well-defined data models and error handling
- Established testing patterns
- Rich ecosystem of CLI libraries (inquirer, rich)

Minor uncertainties:
- OpenRouter API rate limits and specific error handling patterns
- Model performance variations across different Flex code generation tasks
- Complex model filtering UI/UX optimization
- Cross-platform CLI compatibility with interactive features

The extensive language specification, comprehensive OpenRouter documentation, and clear implementation patterns provide strong foundation for successful implementation with dynamic model selection capabilities.