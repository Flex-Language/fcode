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
        spec_path = Path("data/flex_language_spec.json")
        
        try:
            with open(spec_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Flex language spec not found at {spec_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in Flex language spec: {e}")
    
    def _create_agent(self) -> Agent:
        """Create PydanticAI agent with current model and tools."""
        # Get system prompt from flex spec
        system_prompt = self.flex_spec.get('ai_system_prompt', {}).get('description', 
            "You are a Flex programming language expert.")
        
        # Add critical safety instructions
        safety_instructions = self.flex_spec.get('ai_system_prompt', {}).get('CRITICAL_INSTRUCTIONS', {})
        if safety_instructions:
            system_prompt += "\n\nCRITICAL SAFETY INSTRUCTIONS:\n"
            for key, instruction in safety_instructions.items():
                system_prompt += f"- {key}: {instruction}\n"
        
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
    
    async def switch_model(self, model_id: str) -> None:
        """Switch to a different OpenRouter model."""
        # Validate model
        if not self.provider_manager.validate_model_id(model_id):
            raise ValueError(f"Invalid model ID: {model_id}")
        
        # Update current model
        self.current_model_id = model_id
        
        # Recreate agent with new model
        self.agent = self._create_agent()
    
    async def run(self, user_input: str, **kwargs) -> str:
        """Run the agent with user input."""
        deps = AgentDependencies(
            settings=self.settings,
            model_manager=self.model_manager,
            code_validator=self.code_validator,
            flex_executor=self.flex_executor,
            file_manager=self.file_manager,
            session=self.current_session
        )
        
        result = await self.agent.run(user_input, deps=deps)
        return result.data
    
    async def run_stream(self, user_input: str, **kwargs):
        """Run the agent with streaming response."""
        deps = AgentDependencies(
            settings=self.settings,
            model_manager=self.model_manager,
            code_validator=self.code_validator,
            flex_executor=self.flex_executor,
            file_manager=self.file_manager,
            session=self.current_session
        )
        
        async with self.agent.run_stream(user_input, deps=deps) as result:
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