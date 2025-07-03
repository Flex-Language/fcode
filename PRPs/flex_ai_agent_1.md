name: "AI Agent for Flex Programming Language"
description: |

## Purpose
Build a comprehensive AI agent that understands and generates code for the Flex programming language, leveraging the extensive language specification in `data/flex_language_spec.json`. The agent should provide intelligent code generation, error handling, and interactive CLI support with both Franco Arabic and English syntax patterns.

## Core Principles
1. **Context is King**: Include ALL necessary documentation, examples, and caveats from the Flex language spec
2. **Validation Loops**: Provide executable tests/lints the AI can run and fix
3. **Information Dense**: Use keywords and patterns from the Flex specification
4. **Progressive Success**: Start simple, validate, then enhance
5. **Global rules**: Be sure to follow all rules in CLAUDE.md

---

## Goal
Create a production-ready AI agent that can understand, generate, and execute Flex programming language code with full support for both Franco Arabic and English syntax patterns, complete with CLI interface, file operations, and intelligent error handling.

## Why
- **Business value**: Democratizes Flex programming by providing an intelligent assistant
- **Integration**: Bridges cultural and linguistic gaps with dual-syntax support
- **Problems this solves**: 
  - Reduces learning curve for Flex programming
  - Prevents common syntax errors (especially Franco l7d loop safety)
  - Provides contextual help and code generation
  - Enables rapid prototyping and development

## What
A CLI-based AI agent that:
- Generates Flex source files with proper syntax (Franco or English)
- Executes Flex files via CLI (`flex {filename}`)
- Provides intelligent code suggestions and error explanations
- Reads and writes files from the filesystem
- Supports interactive conversations with context memory
- Validates code against Flex language specification

### Success Criteria
- [ ] Agent successfully generates valid Flex code in both Franco and English syntax
- [ ] Agent can execute generated Flex files via CLI
- [ ] Agent provides accurate error explanations and fixes
- [ ] Agent follows Flex best practices (no semicolons, safe loop bounds, etc.)
- [ ] CLI interface is intuitive and responsive
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
  
- url: https://ai.pydantic.dev/multi-agent-applications/
  why: Multi-agent system patterns, dependency injection, tool registration
  
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
│   └── providers.py             # LLM provider configuration
├── tools/
│   ├── __init__.py              # Package initialization
│   ├── flex_executor.py         # Flex CLI execution tool
│   ├── file_manager.py          # File read/write operations
│   └── code_validator.py        # Flex code validation against spec
├── config/
│   ├── __init__.py              # Package initialization
│   └── settings.py              # Environment and configuration management
├── tests/
│   ├── __init__.py              # Package initialization
│   ├── test_flex_agent.py       # Main agent tests
│   ├── test_flex_executor.py    # Executor tool tests
│   ├── test_file_manager.py     # File operations tests
│   ├── test_code_validator.py   # Code validation tests
│   └── test_cli.py              # CLI interface tests
├── cli.py                       # Main CLI interface
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── flex_examples/               # Generated Flex code examples
│   ├── franco_examples/         # Franco Arabic syntax examples
│   └── english_examples/        # English syntax examples
└── README.md                    # Comprehensive project documentation
```

### Known Gotchas of our codebase & Library Quirks
```python
# CRITICAL: Flex Franco l7d loops are INCLUSIVE - must use 'length(array) - 1' for bounds
# Example: karr l7d length(myList) - 1 { } to avoid out-of-bounds errors
# CRITICAL: PydanticAI requires async throughout - no sync functions in async context
# CRITICAL: Use python_dotenv and load_env() for environment variables per CLAUDE.md
# CRITICAL: Never create files longer than 500 lines per CLAUDE.md
# CRITICAL: Always create Pytest unit tests for new features per CLAUDE.md
# CRITICAL: Use relative imports within packages per CLAUDE.md
# CRITICAL: Follow PEP8, use type hints, and format with black per CLAUDE.md
# CRITICAL: Use pydantic for data validation per CLAUDE.md
# CRITICAL: Write docstrings for every function using Google style per CLAUDE.md
# CRITICAL: Flex has mixed syntax support - detect user preference and match their style
# CRITICAL: Use venv_linux virtual environment for Python execution per CLAUDE.md
```

## Implementation Blueprint

### Data models and structure

Create the core data models to ensure type safety and consistency.
```python
# models.py - Core data structures
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any
from enum import Enum

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

class FlexCodeResponse(BaseModel):
    """Response containing generated Flex code."""
    code: str = Field(..., description="Generated Flex code")
    syntax_style: FlexSyntaxStyle = Field(..., description="Detected/used syntax style")
    explanation: str = Field(..., description="Code explanation")
    filename: Optional[str] = Field(None, description="Suggested filename")

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
  - Validate required configuration

CREATE .env.example:
  - Include all required environment variables
  - Add descriptions for each variable
  - Follow CLAUDE.md conventions

Task 2: Create Core Data Models  
CREATE agents/models.py:
  - PATTERN: Use pydantic for data validation per CLAUDE.md
  - Define all request/response models
  - Include proper type hints and validation

Task 3: Implement File Management Tool
CREATE tools/file_manager.py:
  - PATTERN: Async functions for file operations
  - Handle file reading, writing, and validation
  - Support for both .flex and .flx extensions

Task 4: Implement Flex Code Validator
CREATE tools/code_validator.py:
  - PATTERN: Use flex_language_spec.json as validation source
  - Validate syntax patterns (Franco vs English)
  - Check for common errors (l7d loop safety)

Task 5: Implement Flex Executor Tool
CREATE tools/flex_executor.py:
  - PATTERN: Async subprocess execution
  - Handle CLI command: flex {filename}
  - Capture output and errors with proper error handling

Task 6: Create Main Flex Agent
CREATE agents/flex_agent.py:
  - PATTERN: Follow PydanticAI agent creation patterns
  - Load flex_language_spec.json for system prompt
  - Register all tools (@agent.tool decorators)
  - Implement syntax detection and adaptation

Task 7: Implement CLI Interface
CREATE cli.py:
  - PATTERN: Interactive CLI with streaming responses
  - Support conversation history and context
  - Color-coded output for different message types
  - Handle async properly with asyncio.run()

Task 8: Add Comprehensive Tests
CREATE tests/:
  - PATTERN: Mirror project structure in tests
  - Test all major functionality with mocks
  - Include edge cases and error scenarios
  - Achieve 80%+ test coverage

Task 9: Create Documentation and Examples
CREATE README.md:
  - PATTERN: Follow project documentation standards
  - Include setup, installation, and usage instructions
  - Provide example interactions and use cases

CREATE flex_examples/:
  - Generate example Flex programs in both syntax styles
  - Include common patterns and best practices
  - Demonstrate error handling and validation
```

### Per task pseudocode as needed added to each task

```python
# Task 6: Main Flex Agent Implementation
from pydantic_ai import Agent, RunContext
from typing import Any, Dict
import json

# Load Flex language specification
with open('data/flex_language_spec.json', 'r') as f:
    flex_spec = json.load(f)

# Create agent with Flex system prompt
flex_agent = Agent(
    'anthropic:claude-3-5-sonnet-20241022',
    system_prompt=flex_spec['ai_system_prompt']['description'],
    deps_type=AgentDependencies,
    result_type=FlexCodeResponse
)

@flex_agent.tool
async def generate_flex_code(
    ctx: RunContext[AgentDependencies],
    request: FlexCodeRequest
) -> FlexCodeResponse:
    """Generate Flex code based on user request."""
    # PATTERN: Analyze request and determine syntax style
    syntax_style = detect_syntax_preference(request.prompt, request.syntax_style)
    
    # PATTERN: Use flex_language_spec for code generation
    code = generate_code_from_spec(
        request.prompt,
        syntax_style,
        flex_spec['syntax_rules']
    )
    
    # CRITICAL: Validate generated code against spec
    validation_result = validate_flex_code(code, flex_spec)
    if not validation_result.is_valid:
        raise ValidationError(validation_result.errors)
    
    return FlexCodeResponse(
        code=code,
        syntax_style=syntax_style,
        explanation=generate_explanation(code, syntax_style),
        filename=suggest_filename(request.prompt)
    )

@flex_agent.tool
async def execute_flex_code(
    ctx: RunContext[AgentDependencies],
    request: FlexExecutionRequest
) -> FlexExecutionResult:
    """Execute Flex code via CLI."""
    # PATTERN: Save to file if requested
    filename = request.filename or f"temp_{uuid.uuid4().hex[:8]}.flex"
    
    if request.save_to_file:
        await save_flex_file(filename, request.code)
    
    # CRITICAL: Execute with proper error handling
    try:
        result = await subprocess.run(
            ['flex', filename],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return FlexExecutionResult(
            success=result.returncode == 0,
            output=result.stdout,
            error=result.stderr if result.returncode != 0 else None,
            execution_time=time.time() - start_time,
            filename=filename
        )
    except subprocess.TimeoutExpired:
        return FlexExecutionResult(
            success=False,
            output="",
            error="Execution timed out after 30 seconds",
            execution_time=30.0,
            filename=filename
        )

# Task 7: CLI Interface Implementation
async def main():
    """Main CLI interface."""
    print("🚀 Flex AI Agent - Interactive Programming Assistant")
    print("Type 'help' for commands, 'exit' to quit\n")
    
    agent = create_flex_agent()
    conversation_history = []
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                break
            elif user_input.lower() == 'help':
                show_help()
                continue
            
            # PATTERN: Stream response with tool visibility
            async for chunk in agent.run_stream(
                user_input,
                deps=AgentDependencies(history=conversation_history)
            ):
                if chunk.kind == 'response':
                    print(f"🤖 {chunk.content}", end='')
                elif chunk.kind == 'tool-call':
                    print(f"\n🛠 Using tool: {chunk.tool_name}")
                    
            conversation_history.append((user_input, chunk.content))
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
```

### Integration Points
```yaml
ENVIRONMENT:
  - add to: .env
  - vars: |
      # LLM Configuration
      LLM_PROVIDER=anthropic
      LLM_API_KEY=your_api_key_here
      LLM_MODEL=claude-3-5-sonnet-20241022
      
      # Flex Configuration
      FLEX_CLI_PATH=flex
      FLEX_EXAMPLES_DIR=./flex_examples
      FLEX_TEMP_DIR=./temp
      
      # Application Settings
      MAX_CODE_LENGTH=500
      EXECUTION_TIMEOUT=30
      ENABLE_FILE_OPERATIONS=true

DEPENDENCIES:
  - Update requirements.txt with:
    - pydantic-ai
    - pydantic-settings
    - python-dotenv
    - pytest
    - pytest-asyncio
    - pytest-cov
    - black
    - ruff
    - mypy

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
# test_flex_agent.py
async def test_flex_agent_franco_syntax():
    """Test agent generates valid Franco syntax."""
    agent = create_flex_agent()
    request = FlexCodeRequest(
        prompt="create a loop that prints numbers 1 to 10",
        syntax_style=FlexSyntaxStyle.FRANCO
    )
    
    result = await agent.run(request)
    assert result.syntax_style == FlexSyntaxStyle.FRANCO
    assert "karr l7d" in result.code
    assert "etb3" in result.code
    # CRITICAL: Check for safe loop bounds
    assert "length(" in result.code and "- 1" in result.code

async def test_flex_agent_english_syntax():
    """Test agent generates valid English syntax."""
    agent = create_flex_agent()
    request = FlexCodeRequest(
        prompt="create a function that calculates factorial",
        syntax_style=FlexSyntaxStyle.ENGLISH
    )
    
    result = await agent.run(request)
    assert result.syntax_style == FlexSyntaxStyle.ENGLISH
    assert "fun" in result.code
    assert "print" in result.code

async def test_flex_execution():
    """Test Flex code execution."""
    executor = FlexExecutor()
    code = 'etb3("Hello World")'
    
    result = await executor.execute(
        FlexExecutionRequest(code=code, filename="test.flex")
    )
    
    assert result.success
    assert "Hello World" in result.output

def test_syntax_detection():
    """Test automatic syntax detection."""
    # Franco keywords should be detected
    assert detect_syntax_preference("karr l7d 10", FlexSyntaxStyle.AUTO) == FlexSyntaxStyle.FRANCO
    
    # English keywords should be detected
    assert detect_syntax_preference("for i in range(10)", FlexSyntaxStyle.AUTO) == FlexSyntaxStyle.ENGLISH
```

```bash
# Run tests iteratively until passing:
pytest tests/ -v --cov=agents --cov=tools --cov-report=term-missing

# If failing: Debug specific test, fix code, re-run
```

### Level 3: Integration Test
```bash
# Test CLI interaction
python cli.py

# Expected interaction:
# You: Create a simple hello world program in Franco syntax
# 🤖 I'll create a simple hello world program using Franco Arabic syntax.
# 🛠 Using tool: generate_flex_code
# 
# Here's your Flex program:
# ```flex
# etb3("Ahlan wa sahlan - Hello World!")
# ```
# 
# You: Now execute it
# 🤖 I'll execute the Flex program for you.
# 🛠 Using tool: execute_flex_code
# 
# ✅ Execution successful!
# Output: Ahlan wa sahlan - Hello World!

# Test error handling
# You: Create a loop with an error
# 🤖 I notice potential issues with this code...
# 🛠 Using tool: validate_flex_code
# 
# ❌ Error detected: Franco l7d loop safety issue
# Suggestion: Use 'length(array) - 1' for safe bounds
```

## Final Validation Checklist
- [ ] All tests pass: `pytest tests/ -v --cov=agents --cov=tools --cov-report=term-missing`
- [ ] No linting errors: `ruff check .`
- [ ] No type errors: `mypy .`
- [ ] No formatting issues: `black --check .`
- [ ] Agent generates valid Franco syntax
- [ ] Agent generates valid English syntax
- [ ] Agent detects syntax preference correctly
- [ ] Flex CLI execution works properly
- [ ] Error handling and validation work correctly
- [ ] CLI interface is responsive and user-friendly
- [ ] File operations work securely
- [ ] Franco l7d loop safety is enforced
- [ ] README includes comprehensive setup instructions
- [ ] All environment variables documented in .env.example

---

## Anti-Patterns to Avoid
- ❌ Don't ignore Franco l7d loop safety - this is critical
- ❌ Don't use sync functions in async agent context
- ❌ Don't hardcode file paths - use configuration
- ❌ Don't skip input validation - use Pydantic models
- ❌ Don't create files longer than 500 lines per CLAUDE.md
- ❌ Don't forget to create unit tests for new features
- ❌ Don't ignore type hints - use them consistently
- ❌ Don't commit sensitive information like API keys
- ❌ Don't assume flex CLI is installed - validate and document
- ❌ Don't mix syntax styles incorrectly - validate combinations

## Confidence Score: 9/10

High confidence due to:
- Complete Flex language specification available with AI system prompt
- Clear patterns from PydanticAI documentation
- Comprehensive validation approach
- Well-defined data models and error handling
- Established testing patterns

Minor uncertainty around:
- Flex CLI installation and cross-platform compatibility
- Optimal streaming response patterns for complex code generation

The extensive language specification and clear implementation patterns provide strong foundation for successful implementation.