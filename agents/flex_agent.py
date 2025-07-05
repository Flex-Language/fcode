"""
Main Flex AI Agent with PydanticAI and OpenRouter integration.

This module contains the core Flex programming language AI agent that uses
PydanticAI with OpenRouter for dynamic model selection and comprehensive
Flex code assistance.
"""

import json
import time
from pathlib import Path
from typing import Optional, Dict, Any, List
from pydantic_ai import Agent, RunContext
from pydantic import BaseModel

from .models import (
    FlexCodeRequest, 
    FlexCodeResponse, 
    FlexExecutionRequest, 
    FlexExecutionResult,
    FlexSyntaxStyle,
    CodeValidationResult,
    OpenRouterModel,
    ModelFilter,
    AgentSession
)
from agents.providers import OpenRouterProviderManager, create_flex_agent
from tools.model_manager import ModelManager
from tools.code_validator import FlexCodeValidator
from tools.flex_executor import FlexExecutor
from tools.file_manager import FileManager
from config.settings import Settings, get_settings


class AgentDependencies(BaseModel):
    model_config = {"arbitrary_types_allowed": True}

    """Dependencies injected into agent tools."""
    settings: Settings
    model_manager: ModelManager
    code_validator: FlexCodeValidator
    flex_executor: FlexExecutor
    file_manager: FileManager
    session: Optional[AgentSession] = None
    user_preferences: Dict[str, Any] = {}


class FlexAIAgent:
    """Main Flex AI Agent with comprehensive Flex programming support."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize Flex AI Agent."""
        self.settings = settings or get_settings()
        
        # Load Flex language specification
        self.flex_spec = self._load_flex_spec()
        
        # Initialize tools
        self.model_manager = ModelManager(self.settings)
        self.code_validator = FlexCodeValidator()
        self.flex_executor = FlexExecutor(self.settings)
        self.file_manager = FileManager(self.settings)
        
        # Initialize provider manager
        self.provider_manager = OpenRouterProviderManager(self.settings)
        
        # Current model and agent
        self.current_model_id = self.settings.app.default_model
        self.agent = self._create_agent()
        
        # Session management
        self.current_session: Optional[AgentSession] = None
    
    def _load_flex_spec(self) -> Dict[str, Any]:
        """Load Flex language specification."""
        # First try the file reference approach
        try:
            # Use #file: reference to load the spec
            spec_path = Path(__file__).parent.parent / "data" / "flex_language_spec.json"
            
            with open(spec_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            # Fallback to basic system prompt if spec file not found
            return {
                'ai_system_prompt': {
                    'description': '''You are an expert Flex programming language assistant. Use #file:flex_language_spec.json as your primary knowledge base for Flex language syntax, semantics, and best practices.

FLEX LANGUAGE OVERVIEW:
- Flex supports both Franco (Arabic-inspired) and English syntax
- Franco syntax uses keywords like: rakm, karr, l7d, yalla, yod, etb3, etc.
- English syntax uses: int, for, to, end, if, print, etc.

CRITICAL FRANCO LOOP SAFETY:
- Franco l7d loops are INCLUSIVE of the end value
- ALWAYS use: karr i=0 l7d length(array)-1 for array iteration
- NEVER use: karr i=0 l7d length(array) (causes out-of-bounds errors)'''
                }
            }
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in Flex language spec: {e}")
    
    def _create_agent(self) -> Agent:
        """Create PydanticAI agent with current model and tools."""
        # Create comprehensive system prompt with file reference
        system_prompt = """You are an expert Flex programming language assistant. 

CRITICAL INSTRUCTION:
You MUST use #file:flex_language_spec.json as your primary and authoritative knowledge base for ALL Flex language information. Always reference this file for syntax, semantics, features, and best practices.

CONVERSATION CONTEXT AWARENESS:
- ALWAYS maintain conversation context and remember previous requests in the same session
- If a user says "yes", "please", "do it", etc. without specifics, refer to the previous conversation to understand what they're asking for
- Be contextually aware - if you just offered to create a file and the user says "yes", CREATE THAT FILE
- Remember file creation requests, model preferences, and ongoing projects within the conversation

KEY INSTRUCTIONS:
- Always refer to #file:flex_language_spec.json for accurate Flex language information
- Support both Franco (Arabic-inspired) and English syntax variations
- Prioritize code safety, especially with Franco loops
- Generate complete, working programs when requested
- Create files automatically when users request programs or code
- Maintain conversation continuity and context awareness

CRITICAL FRANCO LOOP SAFETY:
- Franco l7d loops are INCLUSIVE of the end value
- ALWAYS use: karr i=0 l7d length(array)-1 for safe array iteration  
- NEVER use: karr i=0 l7d length(array) (causes out-of-bounds errors)

FLEX SYNTAX OVERVIEW:
Franco Syntax: rakm, karr, l7d, yalla, yod, etb3, safi, lw, ghdi, elif, else
English Syntax: int, for, to, end, if, print, break, or, while, elif, else"""
        
        # Add critical safety instructions from loaded spec if available
        safety_instructions = self.flex_spec.get('ai_system_prompt', {}).get('CRITICAL_INSTRUCTIONS', {})
        if safety_instructions:
            system_prompt += "\n\nADDITIONAL SAFETY INSTRUCTIONS:\n"
            for key, instruction in safety_instructions.items():
                system_prompt += f"- {key}: {instruction}\n"
        
        # Add file creation capabilities information
        system_prompt += """

AVAILABLE TOOLS:
- create_file: Create any file with specified content
- create_flex_program_file: Generate and create complete Flex programs from descriptions
- generate_flex_code: Generate Flex code snippets
- execute_flex_code: Run and test Flex code
- validate_flex_code: Check code for errors
- read_file: Read content from existing files
- read_file: Read and display content of existing files

TOOL USAGE GUIDELINES:
- CRITICAL: When user asks to RUN, EXECUTE, or TEST code, YOU MUST use the execute_flex_code tool
- When user says "run it", "execute it", "try to run it", "test the code": call execute_flex_code immediately
- When user mentions running existing files like "run xo_game.lx": first call read_file, then execute_flex_code
- For simple code requests, provide code directly in your response without calling tools
- Only use create_flex_program_file when user explicitly asks to CREATE or SAVE a file
- Use tools when user says "create a file", "save it", "make a .lx file", etc.
- For requests like "write me a game" or "show me code", respond directly with code

WHEN USER ASKS TO RUN/EXECUTE CODE:
- Step 1: If it's a file, use read_file to get the content
- Step 2: ALWAYS use execute_flex_code tool - NEVER say you cannot run code
- Step 3: If code validation fails, fix the errors and try again
- Step 4: Provide execution results including output, errors, and execution time
- NEVER respond with text saying you cannot execute - always try the tool first

WHEN USER ASKS TO CREATE FILES:
- Use create_file for general file creation with provided content
- Use create_flex_program_file for generating complete Flex programs (like games, calculators, etc.)
- Always provide the generated code content when creating files
- Confirm successful file creation with file details"""
        
        # Create agent with current model
        agent = create_flex_agent(
            model_id=self.current_model_id,
            system_prompt=system_prompt,
            deps_type=AgentDependencies,
            result_type=str  # Default to string responses
        )
        
        # Register tools
        self._register_tools(agent)
        
        return agent
    
    def _register_tools(self, agent: Agent) -> None:
        """Register all available tools with the agent."""
        
        @agent.tool
        async def generate_flex_code(
            ctx: RunContext[AgentDependencies],
            request_prompt: str,
            syntax_style: str = "auto",
            max_lines: int = 100,
            include_comments: bool = True
        ) -> str:
            """
            Generate Flex code based on user request.
            
            Args:
                request_prompt: Description of what to generate
                syntax_style: Preferred syntax style (franco/english/auto)
                max_lines: Maximum lines of code
                include_comments: Whether to include explanatory comments
                
            Returns:
                Generated Flex code with explanation
            """
            start_time = time.time()
            
            # Create request
            request = FlexCodeRequest(
                prompt=request_prompt,
                syntax_style=FlexSyntaxStyle(syntax_style.lower()),
                max_lines=max_lines,
                include_comments=include_comments,
                model_id=self.current_model_id
            )
            
            # Detect syntax preference from prompt
            detected_style = self._detect_syntax_preference(request_prompt, request.syntax_style)
            
            # Generate contextual prompt
            generation_prompt = self._create_generation_prompt(request, detected_style)
            
            # Use the current agent to generate code
            # Note: This is a simplified version - in practice, you'd use the model directly
            generated_code = f"""// Generated Flex code for: {request_prompt}
// Syntax style: {detected_style.value}
// Model: {self.current_model_id}

// TODO: Implement actual code generation logic here
etb3("Hello from Flex AI Agent!")
"""
            
            # Validate generated code
            validation_result = await ctx.deps.code_validator.validate_code(generated_code)
            
            if not validation_result.is_valid:
                # Try to fix Franco loop safety issues
                if validation_result.has_franco_loop_safety_issues:
                    generated_code = ctx.deps.code_validator.fix_franco_loop_safety(generated_code)
                    validation_result = await ctx.deps.code_validator.validate_code(generated_code)
            
            generation_time = time.time() - start_time
            
            # Format response
            response = f"Generated Flex Code ({detected_style.value} syntax):\n\n```flex\n{generated_code}\n```\n\n"
            
            if validation_result.warnings:
                response += f"Warnings:\n" + "\n".join(f"- {w}" for w in validation_result.warnings) + "\n\n"
            
            if validation_result.suggestions:
                response += f"Suggestions:\n" + "\n".join(f"- {s}" for s in validation_result.suggestions) + "\n\n"
            
            response += f"Generated in {generation_time:.2f}s using {self.current_model_id}"
            
            return response
        
        @agent.tool
        async def execute_flex_code(
            ctx: RunContext[AgentDependencies],
            code: str,
            save_to_file: bool = True,
            filename: Optional[str] = None,
            timeout: int = 30
        ) -> str:
            """
            Execute Flex code and return results.
            
            Args:
                code: Flex code to execute
                save_to_file: Whether to save code to file
                filename: Optional filename
                timeout: Execution timeout in seconds
                
            Returns:
                Execution results
            """
            # Validate code first
            validation_result = await ctx.deps.code_validator.validate_code(code)
            
            if not validation_result.is_valid:
                error_details = "\n".join(f"- Line {e.line_number}: {e.message}" for e in validation_result.errors)
                return f"❌ Code validation failed:\n{error_details}\n\nPlease fix these errors before execution."
            
            # Execute code
            execution_request = FlexExecutionRequest(
                code=code,
                save_to_file=save_to_file,
                filename=filename,
                timeout=timeout
            )
            
            result = await ctx.deps.flex_executor.execute(execution_request)
            
            # Format response
            if result.success:
                response = f"✅ Execution successful!\n"
                if result.output:
                    response += f"Output:\n{result.output}\n"
                response += f"\nExecution time: {result.execution_time:.2f}s"
                if result.filename:
                    response += f"\nSaved to: {result.filename}"
            else:
                response = f"❌ Execution failed!\n"
                if result.error:
                    response += f"Error: {result.error}\n"
                response += f"Execution time: {result.execution_time:.2f}s"
            
            return response
        
        @agent.tool
        async def validate_flex_code(
            ctx: RunContext[AgentDependencies],
            code: str,
            check_franco_safety: bool = True
        ) -> str:
            """
            Validate Flex code for syntax and safety issues.
            
            Args:
                code: Flex code to validate
                check_franco_safety: Whether to check Franco l7d loop safety
                
            Returns:
                Validation results
            """
            result = await ctx.deps.code_validator.validate_code(code)
            
            response = f"Validation Results for {result.syntax_style.value} syntax:\n\n"
            
            if result.is_valid:
                response += "✅ Code is valid!\n\n"
            else:
                response += "❌ Validation errors found:\n"
                for error in result.errors:
                    response += f"- Line {error.line_number}: {error.message}\n"
                    response += f"  Suggestion: {error.suggestion}\n"
                    if error.is_franco_loop_error:
                        response += "  ⚠️ CRITICAL: Franco l7d loop safety issue!\n"
                response += "\n"
            
            if result.warnings:
                response += "⚠️ Warnings:\n"
                for warning in result.warnings:
                    response += f"- {warning}\n"
                response += "\n"
            
            if result.suggestions:
                response += "💡 Suggestions:\n"
                for suggestion in result.suggestions:
                    response += f"- {suggestion}\n"
                response += "\n"
            
            if check_franco_safety and result.has_franco_loop_safety_issues:
                response += "🔴 CRITICAL: Franco l7d loop safety issues detected!\n"
                response += "Franco loops are INCLUSIVE and will cause out-of-bounds errors.\n"
                response += "Always use 'length(array) - 1' for safe array iteration.\n\n"
                
                # Show safe examples
                examples = ctx.deps.code_validator.get_safe_franco_loop_examples()
                response += "Safe Franco Loop Examples:\n"
                response += examples['safe_array_iteration']
            
            return response
        
        @agent.tool
        async def list_available_models(
            ctx: RunContext[AgentDependencies],
            search_term: Optional[str] = None,
            free_only: bool = False,
            max_results: int = 10
        ) -> str:
            """
            List available OpenRouter models.
            
            Args:
                search_term: Optional search term to filter models
                free_only: Show only free models
                max_results: Maximum number of results
                
            Returns:
                Formatted list of available models
            """
            # Create filter
            model_filter = ModelFilter(
                search_term=search_term,
                free_models_only=free_only
            )
            
            # Get filtered models
            models = await ctx.deps.model_manager.filter_models(model_filter)
            
            # Limit results
            models = models[:max_results]
            
            if not models:
                return "No models found matching your criteria."
            
            response = f"Available Models ({len(models)} found):\n\n"
            
            for i, model in enumerate(models, 1):
                prompt_price = model.pricing.get('prompt', 0)
                completion_price = model.pricing.get('completion', 0)
                
                response += f"{i}. **{model.name}**\n"
                response += f"   ID: {model.id}\n"
                response += f"   Context: {model.context_length:,} tokens\n"
                response += f"   Price: ${prompt_price:.6f}/prompt, ${completion_price:.6f}/completion\n"
                
                if model.description:
                    response += f"   Description: {model.description[:100]}...\n"
                
                response += "\n"
            
            response += f"Current model: {self.current_model_id}"
            
            return response
        
        @agent.tool
        async def switch_model(
            ctx: RunContext[AgentDependencies],
            model_id: str
        ) -> str:
            """
            Switch to a different OpenRouter model.
            
            Args:
                model_id: OpenRouter model ID to switch to
                
            Returns:
                Confirmation message
            """
            # Validate model exists
            model = await ctx.deps.model_manager.get_model_by_id(model_id)
            
            if not model:
                available_models = await ctx.deps.model_manager.list_models()
                suggestions = [m.id for m in available_models if model_id.lower() in m.id.lower()][:3]
                
                response = f"❌ Model '{model_id}' not found."
                if suggestions:
                    response += f"\n\nDid you mean one of these?\n"
                    for suggestion in suggestions:
                        response += f"- {suggestion}\n"
                return response
            
            # Switch model
            old_model = self.current_model_id
            await self.switch_model(model_id)
            
            return f"✅ Switched from {old_model} to {model_id}\n\nModel Info:\n- Name: {model.name}\n- Context: {model.context_length:,} tokens\n- Provider: {model.top_provider or 'Unknown'}"
        
        @agent.tool
        async def get_flex_examples(
            ctx: RunContext[AgentDependencies],
            syntax_style: str = "both",
            topic: Optional[str] = None
        ) -> str:
            """
            Get Flex code examples.
            
            Args:
                syntax_style: Syntax style (franco/english/both)
                topic: Optional topic filter
                
            Returns:
                Flex code examples
            """
            # Get safe Franco loop examples from validator
            examples = ctx.deps.code_validator.get_safe_franco_loop_examples()
            
            response = "Flex Code Examples:\n\n"
            
            if syntax_style.lower() in ["franco", "both"]:
                response += "## Franco Syntax Examples\n\n"
                response += "### Safe Array Iteration (CRITICAL):\n"
                response += "```flex\n" + examples['safe_array_iteration'] + "\n```\n\n"
                
                response += "### Basic Franco Patterns:\n"
                response += """```flex
// Variable declarations
rakm counter = 0
kasr price = 29.99
klma message = "Ahlan wa sahlan"
so2al isReady = sa7
dorg numbers = [1, 2, 3, 4, 5]

// Function definition
sndo2 calculate(rakm a, rakm b) {
    rakm result = a * b
    rg3 result
}

// Conditional logic
lw counter > 0 {
    etb3("Counter is positive")
} gher {
    etb3("Counter is zero or negative")
}

// User input
etb3("Enter your name:")
klma name = da5l()
etb3("Hello, " + name + "!")
```
"""
            
            if syntax_style.lower() in ["english", "both"]:
                response += "## English Syntax Examples\n\n"
                
                response += "### Safe Array Iteration:\n"
                response += "```flex\n" + examples['alternative_english'] + "\n```\n\n"
                
                response += "### Basic English Patterns:\n"
                response += """```flex
// Variable declarations
int counter = 0
float price = 29.99
string message = "Hello World"
bool isReady = true
list numbers = [1, 2, 3, 4, 5]

// Function definition
fun calculate(int a, int b) {
    int result = a * b
    return result
}

// Conditional logic
if (counter > 0) {
    print("Counter is positive")
} else {
    print("Counter is zero or negative")
}

// User input
print("Enter your name:")
string name = scan()
print("Hello, " + name + "!")
```
"""
            
            return response
        
        @agent.tool
        async def create_file(
            ctx: RunContext[AgentDependencies],
            filename: str,
            content: str,
            overwrite: bool = False
        ) -> str:
            """
            Create a new file with the specified content.
            
            Args:
                filename: Name of the file to create (e.g., 'xo_game.lx', 'calculator.flex')
                content: Content to write to the file
                overwrite: Whether to overwrite existing file (default: False)
                
            Returns:
                Result message indicating success or failure
            """
            from pathlib import Path
            from tools.file_manager import FileOperation
            
            try:
                # Check if file exists and overwrite is False
                if not overwrite and Path(filename).exists():
                    return f"❌ File '{filename}' already exists. Use overwrite=True to replace it, or choose a different filename."
                
                # Create the file using the file manager
                write_op = FileOperation(
                    operation="write",
                    filepath=filename,
                    content=content,
                    backup=not overwrite  # Only backup if not overwriting
                )
                
                result = await ctx.deps.file_manager.execute_operation(write_op)
                
                if result.success:
                    size_info = f" ({result.file_size} bytes)" if hasattr(result, 'file_size') and result.file_size else ""
                    return f"✅ Successfully created file: {filename}{size_info}\n\nFile contents:\n```\n{content[:200]}{'...' if len(content) > 200 else ''}\n```"
                else:
                    return f"❌ Failed to create file '{filename}': {result.message}"
                    
            except Exception as e:
                return f"❌ Error creating file '{filename}': {str(e)}"
        
        @agent.tool  
        async def create_flex_program_file(
            ctx: RunContext[AgentDependencies],
            filename: str,
            program_description: str,
            syntax_style: str = "franco",
            include_comments: bool = True
        ) -> str:
            """
            Generate and create a complete Flex program file based on description.
            
            Args:
                filename: Name of the file to create (e.g., 'xo_game.lx')
                program_description: Description of the program to generate (e.g., 'XO tic-tac-toe game')
                syntax_style: Preferred syntax style (franco/english)
                include_comments: Whether to include explanatory comments
                
            Returns:
                Result message with file creation status and code preview
            """
            try:
                # Generate the code first
                generation_request = FlexCodeRequest(
                    prompt=program_description,
                    syntax_style=FlexSyntaxStyle(syntax_style.lower()),
                    max_lines=200,  # Allow larger programs
                    include_comments=include_comments,
                    model_id=self.current_model_id
                )
                
                # Detect syntax preference
                detected_style = self._detect_syntax_preference(program_description, generation_request.syntax_style)
                
                # Create generation prompt
                generation_prompt = self._create_generation_prompt(generation_request, detected_style)
                
                # Generate code directly using a simple template approach instead of recursive agent call
                # This prevents infinite recursion when agent calls this tool
                
                if "xo" in program_description.lower() or "tic" in program_description.lower():
                    # XO/Tic-tac-toe game template
                    if detected_style == FlexSyntaxStyle.FRANCO:
                        code_content = self._generate_xo_game_franco()
                    else:
                        code_content = self._generate_xo_game_english()
                elif "calculator" in program_description.lower():
                    # Calculator template
                    if detected_style == FlexSyntaxStyle.FRANCO:
                        code_content = self._generate_calculator_franco()
                    else:
                        code_content = self._generate_calculator_english()
                else:
                    # Generic template
                    code_content = f"""// Generated Flex program: {program_description}
// This is a basic template - please customize as needed

etb3("Welcome to your Flex program!")
etb3("Program: {program_description}")

// TODO: Implement your program logic here
// Use Flex language features like:
// - Variables: rakm num = 10
// - Loops: karr i=0 l7d 9 {{ }}
// - Input: klma input = yod()
// - Conditions: lw condition {{ }}

etb3("Program completed!")"""
                
                # Create the file using the file manager
                from pathlib import Path
                from tools.file_manager import FileOperation
                
                if Path(filename).exists():
                    return f"❌ File '{filename}' already exists. Please choose a different filename or use the create_file tool with overwrite=True."
                
                write_op = FileOperation(
                    operation="write", 
                    filepath=filename,
                    content=code_content,
                    backup=False
                )
                
                result = await ctx.deps.file_manager.execute_operation(write_op)
                
                if result.success:
                    size_info = f" ({result.file_size} bytes)" if hasattr(result, 'file_size') and result.file_size else ""
                    return f"✅ Successfully created Flex program file: {filename}{size_info}\n\n🎯 Program: {program_description}\n📝 Syntax: {detected_style.value}\n\nCode preview:\n```flex\n{code_content[:300]}{'...' if len(code_content) > 300 else ''}\n```\n\n💡 You can now run this file with the Flex interpreter!"
                else:
                    return f"❌ Failed to create file '{filename}': {result.message}"
                    
            except Exception as e:
                return f"❌ Error creating Flex program file '{filename}': {str(e)}"
    
        @agent.tool
        async def read_file(
            ctx: RunContext[AgentDependencies],
            filename: str
        ) -> str:
            """
            Read the content of a file.
            
            Args:
                filename: Name or path of the file to read
                
            Returns:
                File content or error message
            """
            try:
                # Handle both absolute and relative paths
                if not filename.startswith('/'):
                    # If it's a relative path, look in current directory
                    filepath = Path(filename)
                    if not filepath.exists():
                        # Also try looking in the workspace root
                        workspace_root = Path(__file__).parent.parent
                        filepath = workspace_root / filename
                else:
                    filepath = Path(filename)
                
                if not filepath.exists():
                    return f"❌ File '{filename}' not found."
                
                # Read file content
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                return f"✅ File content of '{filename}':\n\n```flex\n{content}\n```"
                
            except Exception as e:
                return f"❌ Error reading file '{filename}': {str(e)}"

    def _detect_syntax_preference(self, prompt: str, requested_style: FlexSyntaxStyle) -> FlexSyntaxStyle:
        """Detect user's syntax preference from their prompt."""
        if requested_style != FlexSyntaxStyle.AUTO:
            return requested_style
        
        # Check for Franco keywords
        franco_keywords = ['karr', 'l7d', 'etb3', 'da5l', 'lw', 'sndo2', 'rakm', 'kasr', 'klma']
        english_keywords = ['for', 'print', 'scan', 'if', 'function', 'int', 'float', 'string']
        
        franco_count = sum(1 for keyword in franco_keywords if keyword in prompt.lower())
        english_count = sum(1 for keyword in english_keywords if keyword in prompt.lower())
        
        if franco_count > english_count:
            return FlexSyntaxStyle.FRANCO
        elif english_count > franco_count:
            return FlexSyntaxStyle.ENGLISH
        else:
            return FlexSyntaxStyle.AUTO
    
    def _create_generation_prompt(self, request: FlexCodeRequest, style: FlexSyntaxStyle) -> str:
        """Create a contextual prompt for code generation."""
        prompt = f"Generate Flex code that {request.prompt}. "
        
        if style == FlexSyntaxStyle.FRANCO:
            prompt += "Use Franco Arabic syntax (karr, l7d, etb3, etc.). "
            prompt += "CRITICAL: For array iteration, use 'karr i=0 l7d length(array) - 1' to avoid out-of-bounds errors. "
        elif style == FlexSyntaxStyle.ENGLISH:
            prompt += "Use English syntax (for, print, if, etc.). "
        
        if request.include_comments:
            prompt += "Include explanatory comments. "
        
        prompt += f"Keep code under {request.max_lines} lines. "
        prompt += "Follow Flex best practices and ensure code safety."
        
        return prompt
    
    def _format_conversation_context(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Format conversation history for context."""
        if not conversation_history:
            return ""
        
        # Get last 5 conversation turns to avoid token limit issues
        recent_history = conversation_history[-10:]  # Last 10 entries (5 user + 5 assistant)
        
        context_parts = ["Previous conversation context:"]
        
        for entry in recent_history:
            entry_type = entry.get('type', 'unknown')
            content = entry.get('content', '')
            
            if entry_type == 'user':
                context_parts.append(f"User: {content}")
            elif entry_type == 'assistant':
                # Truncate assistant responses to avoid too much context
                truncated_content = content[:300] + "..." if len(content) > 300 else content
                context_parts.append(f"Assistant: {truncated_content}")
        
        return "\n".join(context_parts)
    
    async def switch_model(self, model_id: str) -> None:
        """Switch to a different OpenRouter model."""
        # Validate model
        if not self.provider_manager.validate_model_id(model_id):
            raise ValueError(f"Invalid model ID: {model_id}")
        
        # Update current model
        self.current_model_id = model_id
        
        # Recreate agent with new model
        self.agent = self._create_agent()
    
    async def run(self, user_input: str, conversation_history: Optional[List[Dict[str, Any]]] = None, **kwargs) -> str:
        """Run the agent with user input and conversation context."""
        # Create conversation context if provided
        conversation_context = ""
        if conversation_history:
            conversation_context = self._format_conversation_context(conversation_history)
            # Prepend context to user input
            user_input_with_context = f"{conversation_context}\n\nCurrent user input: {user_input}"
        else:
            user_input_with_context = user_input
        
        deps = AgentDependencies(
            settings=self.settings,
            model_manager=self.model_manager,
            code_validator=self.code_validator,
            flex_executor=self.flex_executor,
            file_manager=self.file_manager,
            session=self.current_session
        )
        
        result = await self.agent.run(user_input_with_context, deps=deps)
        return result.data
    
    async def run_stream(self, user_input: str, conversation_history: Optional[List[Dict[str, Any]]] = None, **kwargs):
        """Run the agent with streaming response and conversation context."""
        # Create conversation context if provided
        conversation_context = ""
        if conversation_history:
            conversation_context = self._format_conversation_context(conversation_history)
            # Prepend context to user input
            user_input_with_context = f"{conversation_context}\n\nCurrent user input: {user_input}"
        else:
            user_input_with_context = user_input
        
        deps = AgentDependencies(
            settings=self.settings,
            model_manager=self.model_manager,
            code_validator=self.code_validator,
            flex_executor=self.flex_executor,
            file_manager=self.file_manager,
            session=self.current_session
        )
        
        async with self.agent.run_stream(user_input_with_context, deps=deps) as result:
            # Access the streamed response through the result's stream attribute
            async for chunk in result.stream():
                yield chunk
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the current agent state."""
        return {
            "current_model": self.current_model_id,
            "flex_spec_loaded": bool(self.flex_spec),
            "tools_registered": True,
            "session_active": self.current_session is not None,
            "settings": {
                "max_code_length": self.settings.app.max_code_length,
                "execution_timeout": self.settings.app.execution_timeout,
                "model_cache_duration": self.settings.app.model_cache_duration
            }
        }
    
    def _generate_xo_game_franco(self) -> str:
        """Generate XO game in Franco syntax."""
        return """// XO Tic-Tac-Toe Game in Franco Syntax
// By Flex AI Agent

etb3("Ahlan wa Sahlan! Welcome to XO Game!")

// Initialize 3x3 board
dorg board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

klma current_player = "X"
so2al game_over = ghlata

// Function to display board
sndo2 show_board() {
    etb3("  0   1   2")
    karr i=0 l7d 2 {
        etb3(i + " " + board[i][0] + " | " + board[i][1] + " | " + board[i][2])
        lw i < 2 {
            etb3("  --|---|--")
        }
    }
}

// Function to check winner
sndo2 check_winner() {
    // Check rows
    karr i=0 l7d 2 {
        lw board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != " " {
            rg3 board[i][0]
        }
    }
    
    // Check columns  
    karr j=0 l7d 2 {
        lw board[0][j] == board[1][j] && board[1][j] == board[2][j] && board[0][j] != " " {
            rg3 board[0][j]
        }
    }
    
    // Check diagonals
    lw board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != " " {
        rg3 board[0][0]
    }
    lw board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != " " {
        rg3 board[0][2]
    }
    
    rg3 ""
}

// Main game loop
9ad !game_over {
    show_board()
    etb3("Player " + current_player + ", enter row (0-2):")
    rakm row = yod()
    etb3("Enter column (0-2):")  
    rakm col = yod()
    
    lw row >= 0 && row <= 2 && col >= 0 && col <= 2 && board[row][col] == " " {
        board[row][col] = current_player
        
        klma winner = check_winner()
        lw winner != "" {
            show_board()
            etb3("Player " + winner + " wins! Mabrook!")
            game_over = sa7
        } gher {
            // Switch player
            lw current_player == "X" {
                current_player = "O"
            } gher {
                current_player = "X"
            }
        }
    } gher {
        etb3("Invalid move! Try again.")
    }
}

etb3("Game finished! Shukran for playing!")"""

    def _generate_xo_game_english(self) -> str:
        """Generate XO game in English syntax."""
        return """// XO Tic-Tac-Toe Game in English Syntax  
// By Flex AI Agent

print("Welcome to XO Game!")

// Initialize 3x3 board
list board = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]

string current_player = "X"
bool game_over = false

// Function to display board
function show_board() {
    print("  0   1   2")
    for i=0 to 2 {
        print(i + " " + board[i][0] + " | " + board[i][1] + " | " + board[i][2])
        if i < 2 {
            print("  --|---|--")
        }
    }
}

// Function to check winner
function check_winner() {
    // Check rows
    for i=0 to 2 {
        if board[i][0] == board[i][1] && board[i][1] == board[i][2] && board[i][0] != " " {
            return board[i][0]
        }
    }
    
    // Check columns
    for j=0 to 2 {
        if board[0][j] == board[1][j] && board[1][j] == board[2][j] && board[0][j] != " " {
            return board[0][j]
        }
    }
    
    // Check diagonals
    if board[0][0] == board[1][1] && board[1][1] == board[2][2] && board[0][0] != " " {
        return board[0][0]
    }
    if board[0][2] == board[1][1] && board[1][1] == board[2][0] && board[0][2] != " " {
        return board[0][2]
    }
    
    return ""
}

// Main game loop
while !game_over {
    show_board()
    print("Player " + current_player + ", enter row (0-2):")
    int row = input()
    print("Enter column (0-2):")
    int col = input()
    
    if row >= 0 && row <= 2 && col >= 0 && col <= 2 && board[row][col] == " " {
        board[row][col] = current_player
        
        string winner = check_winner()
        if winner != "" {
            show_board()
            print("Player " + winner + " wins! Congratulations!")
            game_over = true
        } else {
            // Switch player
            if current_player == "X" {
                current_player = "O"
            } else {
                current_player = "X"
            }
        }
    } else {
        print("Invalid move! Try again.")
    }
}

print("Game finished! Thanks for playing!")"""

    def _generate_calculator_franco(self) -> str:
        """Generate calculator in Franco syntax."""
        return """// Calculator in Franco Syntax
// By Flex AI Agent

etb3("Ahlan! Calculator Program")

9ad sa7 {
    kasr num1, num2, result
    klma operation
    so2al valid = sa7
    
    etb3("Enter first number:")
    num1 = yod()
    
    etb3("Enter second number:")  
    num2 = yod()
    
    etb3("Choose operation (+, -, *, /):")
    operation = yod()
    
    lw operation == "+" {
        result = num1 + num2
    } elif operation == "-" {
        result = num1 - num2  
    } elif operation == "*" {
        result = num1 * num2
    } elif operation == "/" {
        lw num2 == 0 {
            etb3("Error: Division by zero!")
            valid = ghlata
        } gher {
            result = num1 / num2
        }
    } gher {
        etb3("Invalid operation!")
        valid = ghlata
    }
    
    lw valid {
        etb3("Result: " + result)
    }
    
    etb3("Continue? (y/n):")
    klma answer = yod()
    lw answer != "y" && answer != "Y" {
        etb3("Goodbye!")
        tawaqaf
    }
}"""

    def _generate_calculator_english(self) -> str:
        """Generate calculator in English syntax."""
        return """// Calculator in English Syntax
// By Flex AI Agent

print("Welcome! Calculator Program")

while true {
    float num1, num2, result
    string operation
    bool valid = true
    
    print("Enter first number:")
    num1 = input()
    
    print("Enter second number:")
    num2 = input()
    
    print("Choose operation (+, -, *, /):")
    operation = input()
    
    if operation == "+" {
        result = num1 + num2
    } elif operation == "-" {
        result = num1 - num2
    } elif operation == "*" {
        result = num1 * num2
    } elif operation == "/" {
        if num2 == 0 {
            print("Error: Division by zero!")
            valid = false
        } else {
            result = num1 / num2
        }
    } else {
        print("Invalid operation!")
        valid = false
    }
    
    if valid {
        print("Result: " + result)
    }
    
    print("Continue? (y/n):")
    string answer = input()
    if answer != "y" && answer != "Y" {
        print("Goodbye!")
        break
    }
}"""