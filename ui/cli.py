"""
Main CLI Interface for Flex AI Agent.

This module provides the interactive command-line interface for the Flex AI Agent
with streaming responses, model selection, and comprehensive Flex programming support.
"""

import asyncio
import sys
from typing import List, Dict, Any, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.markdown import Markdown

from agents.flex_agent import FlexAIAgent
from tools.model_manager import ModelManager
from ui.model_selector import ModelSelector
from config.settings import get_settings, validate_settings
from ui import formatters


class FlexCLI:
    """Main CLI interface for Flex AI Agent."""
    
    def __init__(self):
        """Initialize CLI interface."""
        self.console = Console()
        self.settings = get_settings()
        
        # Initialize components
        self.agent: Optional[FlexAIAgent] = None
        self.model_manager: Optional[ModelManager] = None
        self.model_selector: Optional[ModelSelector] = None
        
        # Session state
        self.conversation_history: List[Dict[str, Any]] = []
        self.is_running = False
        
        # Commands
        self.commands = {
            'help': self._show_help,
            'models': self._model_selection_menu,
            'switch': self._switch_model_command,
            'validate': self._validate_code_command,
            'execute': self._execute_code_command,
            'examples': self._show_examples_command,
            'settings': self._show_settings,
            'clear': self._clear_conversation,
            'history': self._show_history,
            'save': self._save_conversation,
            'exit': self._exit_command,
            'quit': self._exit_command
        }
    
    async def start(self) -> None:
        """Start the CLI interface."""
        try:
            # Validate settings first
            validate_settings(self.settings)
            
            # Initialize components
            await self._initialize_components()
            
            # Show welcome message
            self._show_welcome()
            
            # Start main loop
            self.is_running = True
            await self._main_loop()
            
        except KeyboardInterrupt:
            self.is_running = False
            # Clean exit message
            self.console.print("\n👋 Goodbye!")
        except Exception as e:
            formatters.display_error(f"Fatal error: {e}")
            sys.exit(1)
        finally:
            self.is_running = False
    
    async def _initialize_components(self) -> None:
        """Initialize all components."""
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console,
            transient=True
        ) as progress:
            
            # Initialize model manager
            progress.add_task(description="Initializing model manager...", total=None)
            self.model_manager = ModelManager(self.settings)
            
            # Initialize model selector
            progress.add_task(description="Setting up model selection...", total=None)
            self.model_selector = ModelSelector(self.model_manager, self.settings)
            
            # Initialize agent
            progress.add_task(description="Loading Flex AI Agent...", total=None)
            self.agent = FlexAIAgent(self.settings)
            
            # Test OpenRouter connection
            progress.add_task(description="Testing OpenRouter connection...", total=None)
            try:
                models = await self.model_manager.list_models()
                if not models:
                    raise Exception("No models available")
            except Exception as e:
                raise Exception(f"OpenRouter connection failed: {e}")
    
    def _show_welcome(self) -> None:
        """Show welcome message and current status."""
        welcome_message = (
            "Welcome to the Flex programming language AI assistant!\n"
            "Type 'help' for commands, 'models' for model selection, or ask me anything about Flex programming.\n\n"
            f"Current model: [bold]{self.agent.current_model_id}[/bold]\n"
            "💡 This agent uses #file:flex_language_spec.json as its comprehensive knowledge base for accurate Flex programming assistance."
        )
        formatters.display_message(welcome_message, title="Flex AI Agent")
    
    async def _main_loop(self) -> None:
        """Main interaction loop."""
        # Check API key status on first run
        await self._check_api_key_status()
        
        while self.is_running:
            try:
                # Get user input with proper EOF handling
                try:
                    user_input = Prompt.ask("You", console=self.console).strip()
                except EOFError:
                    # Handle EOF gracefully (Ctrl+D or end of input)
                    self.console.print("\n👋 Goodbye!")
                    self.is_running = False
                    break
                except Exception as input_error:
                    # Handle other input errors
                    formatters.display_error(f"Input error: {input_error}")
                    # Add a small delay to prevent rapid error loops
                    await asyncio.sleep(0.1)
                    continue
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.startswith('/'):
                    await self._handle_command(user_input[1:])
                elif user_input.lower() in self.commands:
                    await self.commands[user_input.lower()]()
                else:
                    # Process as AI request
                    await self._process_ai_request(user_input)
                
            except KeyboardInterrupt:
                try:
                    self.console.print()  # New line for cleaner output
                    if Confirm.ask("🤔 Do you want to exit?", default=False):
                        self.is_running = False
                        break
                    else:
                        formatters.display_message("Continuing...", title="Info")
                except (KeyboardInterrupt, EOFError):
                    # Second Ctrl+C or EOF - force exit cleanly
                    self.console.print("\n👋 Goodbye!")
                    self.is_running = False
                    break
            except Exception as e:
                formatters.display_error(f"Error: {e}")
                
        # Clean exit (remove the extra "Thank you" message since we handle it in start())
        if self.is_running:
            self.is_running = False
    
    async def _handle_command(self, command_line: str) -> None:
        """Handle slash commands."""
        parts = command_line.split()
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        if command in self.commands:
            if command in ['switch'] and args:
                await self._switch_model_command(' '.join(args))
            else:
                await self.commands[command]()
        else:
            formatters.display_error(f"Unknown command: /{command}\nType 'help' for available commands.")
    
    async def _process_ai_request(self, user_input: str) -> None:
        """Process user request with the AI agent."""
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user',
            'content': user_input,
            'timestamp': asyncio.get_event_loop().time()
        })
        
        try:
            # Add timeout wrapper for AI requests with more reasonable timeout
            timeout_seconds = 120  # Increased to 120 seconds for complex requests
            
            # Show loading indicator while waiting
            self.console.print("🤖 Assistant: thinking...", style="cyan dim")
            
            response_content = ""
            
            # Create timeout task for streaming
            async def process_stream():
                nonlocal response_content
                
                try:
                    chunk_count = 0
                    has_content = False
                    async for chunk in self.agent.run_stream(user_input):
                        chunk_count += 1
                        
                        # PydanticAI returns cumulative strings
                        current_content = str(chunk)
                        
                        # Check if we're getting actual content
                        if current_content.strip():
                            has_content = True
                            
                        # Check if we're getting empty chunks (streaming issue)
                        if chunk_count > 5 and not has_content:
                            # Streaming is returning empty chunks, fall back to non-streaming
                            raise ValueError("Streaming returned empty chunks")
                        
                        response_content = current_content
                    
                    # If we got no meaningful content from streaming, try non-streaming
                    if not response_content.strip():
                        raise ValueError("Streaming produced no content")
                        
                except Exception as e:
                    raise e
                
                return response_content
            
            # Execute with timeout
            try:
                response_content = await asyncio.wait_for(
                    process_stream(), 
                    timeout=timeout_seconds
                )
            except asyncio.TimeoutError:
                raise
            
            # Clear the thinking indicator and display the formatted response
            self.console.print("\r", end="")  # Clear the line
            
            # Use the enhanced formatter to display the response
            formatters.display_enhanced_ai_response(response_content, self.agent.current_model_id)
            
            # Add response to history
            self.conversation_history.append({
                'type': 'assistant',
                'content': response_content,
                'model': self.agent.current_model_id,
                'timestamp': asyncio.get_event_loop().time()
            })
            
        except asyncio.TimeoutError:
            self.console.print("\r", end="")  # Clear the line
            formatters.display_error(f"Request timed out after {timeout_seconds} seconds. The AI service may be busy.")
            formatters.display_message(
                "💡 Try a simpler request or check your internet connection.", 
                title="Suggestion"
            )
            
            # Try fallback non-streaming approach
            try:
                self.console.print("Trying fallback method...", style="dim")
                fallback_response = await asyncio.wait_for(
                    self.agent.run(user_input), 
                    timeout=30
                )
                self.console.print("\r", end="")  # Clear the line
                
                # Use enhanced formatting for fallback response too
                formatters.display_enhanced_ai_response(fallback_response, self.agent.current_model_id)
                
                # Add to history
                self.conversation_history.append({
                    'type': 'assistant',
                    'content': fallback_response,
                    'model': self.agent.current_model_id,
                    'timestamp': asyncio.get_event_loop().time()
                })
                
            except asyncio.CancelledError:
                # Handle cancellation gracefully
                self.console.print("\r", end="")  # Clear the line
                formatters.display_message("Request cancelled.", title="Info")
            except Exception as fallback_error:
                formatters.display_error(f"Fallback also failed:")
                formatters.display_message(
                    "You can still use offline features like 'validate', 'models', 'help'.",
                    title="Offline Mode"
                )
        except asyncio.CancelledError:
            # Handle cancellation during main request
            self.console.print("\r", end="")  # Clear the line
            formatters.display_message("Request cancelled.", title="Info")
        except Exception as e:
            self.console.print("\r", end="")  # Clear the line
            error_msg = str(e)
            
            # Check if this is a streaming issue that we can handle with fallback
            if "streaming" in error_msg.lower() or "empty chunks" in error_msg.lower() or "no content" in error_msg.lower():
                try:
                    self.console.print("Streaming failed, trying direct method...", style="dim")
                    fallback_response = await asyncio.wait_for(
                        self.agent.run(user_input), 
                        timeout=60
                    )
                    self.console.print("\r", end="")  # Clear the line
                    
                    # Use enhanced formatting for fallback response
                    formatters.display_enhanced_ai_response(fallback_response, self.agent.current_model_id)
                    
                    # Add to history
                    self.conversation_history.append({
                        'type': 'assistant',
                        'content': fallback_response,
                        'model': self.agent.current_model_id,
                        'timestamp': asyncio.get_event_loop().time()
                    })
                    return  # Success, don't show error
                    
                except asyncio.CancelledError:
                    # Handle cancellation in fallback
                    self.console.print("\r", end="")  # Clear the line
                    formatters.display_message("Request cancelled.", title="Info")
                    return
                except Exception as fallback_error:
                    formatters.display_error(f"Both streaming and direct methods failed: {fallback_error}")
            
            # Provide helpful error messages for common issues
            elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                formatters.display_error("API authentication failed. Please check your OpenRouter API key.")
                formatters.display_message(
                    "Set OPENROUTER_API_KEY environment variable or check https://openrouter.ai/",
                    title="Help"
                )
            elif "rate limit" in error_msg.lower():
                formatters.display_error("Rate limit exceeded. Please wait a moment before trying again.")
            elif "network" in error_msg.lower() or "connection" in error_msg.lower():
                formatters.display_error("Network connection issue. Please check your internet connection.")
            else:
                formatters.display_error(f"Error processing request: {error_msg}")
                formatters.display_message(
                    "You can still use offline features like code validation and file operations.",
                    title="Offline Mode Available"
                )
    
    async def _check_api_key_status(self) -> None:
        """Check API key status and provide user guidance."""
        try:
            api_key = self.settings.openrouter.api_key
            if not api_key or api_key.strip() == "":
                formatters.display_message(
                    "⚠️  No OpenRouter API key found. AI features will be limited.\n"
                    "To enable AI code generation:\n"
                    "1. Get a free API key from https://openrouter.ai/\n"
                    "2. Set: export OPENROUTER_API_KEY='your-key'\n"
                    "3. Restart the application\n\n"
                    "You can still use: models, validate, examples, and help commands.",
                    title="API Key Status"
                )
            else:
                formatters.display_message(
                    "✅ OpenRouter API key found. AI features are enabled!\n"
                    "Try asking: 'write me a Franco loop' or 'create a calculator'",
                    title="AI Ready"
                )
        except Exception as e:
            formatters.display_error(f"Error checking API status: {e}")
    
    async def _show_help(self) -> None:
        """Show help information."""
        help_text = """
# Flex AI Agent Commands

## Basic Commands
- `help` - Show this help message
- `models` - Open interactive model selection
- `switch <model_id>` - Switch to specific model
- `examples` - Show Flex code examples
- `clear` - Clear conversation history
- `exit` / `quit` - Exit the application

## Flex Programming Commands
- `validate <code>` - Validate Flex code
- `execute <code>` - Execute Flex code
- `/validate` - Interactive code validation
- `/execute` - Interactive code execution

## Utility Commands
- `settings` - Show current settings
- `history` - Show conversation history
- `save` - Save conversation to file

## Usage Tips
- Ask questions about Flex programming in natural language
- Request code generation: "Create a loop in Franco syntax"
- Get help with errors: "Why is my Franco loop causing errors?"
- Switch between Franco and English syntax as needed

## Franco Loop Safety
⚠️ **CRITICAL**: Franco l7d loops are INCLUSIVE!
- Use `karr i=0 l7d length(array) - 1` for safe array iteration
- Never use `karr i=0 l7d length(array)` as it causes out-of-bounds errors

Type any question or request to get started!
"""
        
        self.console.print(Markdown(help_text))
    
    async def _model_selection_menu(self) -> None:
        """Open interactive model selection."""
        if not self.model_selector:
            formatters.display_error("Model selector not available.")
            return
        
        try:
            selected_model = await self.model_selector.select_model_interactive(
                current_model=self.agent.current_model_id
            )
            
            if selected_model and selected_model != self.agent.current_model_id:
                await self.agent.switch_model(selected_model)
                formatters.display_message(f"Switched to model: {selected_model}", title="Model Switch")
            
        except Exception as e:
            formatters.display_error(f"Model selection failed: {e}")
    
    async def _switch_model_command(self, model_id: Optional[str] = None) -> None:
        """Switch to a specific model."""
        if not model_id:
            model_id = Prompt.ask("Enter model ID")
        
        if not model_id:
            return
        
        try:
            await self.agent.switch_model(model_id)
            formatters.display_message(f"Switched to model: {model_id}", title="Model Switch")
            
        except Exception as e:
            formatters.display_error(f"Failed to switch model: {e}")
            
            # Suggest similar models
            try:
                models = await self.model_manager.list_models()
                suggestions = [m.id for m in models if model_id.lower() in m.id.lower()][:3]
                if suggestions:
                    suggestion_text = "Did you mean one of these?\n" + "\n".join([f"- {s}" for s in suggestions])
                    formatters.display_message(suggestion_text, title="Suggestions")
            except:
                pass
    
    async def _validate_code_command(self, code: Optional[str] = None) -> None:
        """Validate Flex code."""
        if not code:
            self.console.print("Enter Flex code to validate (press Ctrl+D when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                code = '\n'.join(lines)
        
        if not code:
            return
        
        # Use agent's validation tool
        result = await self.agent.validate_code(code)
        formatters.display_validation_result(result)
    
    async def _execute_code_command(self, code: Optional[str] = None) -> None:
        """Execute Flex code."""
        if not code:
            self.console.print("Enter Flex code to execute (press Ctrl+D when done):")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                code = '\n'.join(lines)
        
        if not code:
            return
        
        # Confirm execution
        if not Confirm.ask("🚀 Execute this Flex code?", default=True):
            return
        
        # Use agent's execution tool
        result = await self.agent.execute_code(code)
        formatters.display_execution_result(result)
    
    async def _show_examples_command(self) -> None:
        """Show Flex code examples."""
        result = await self.agent.run("show me Flex code examples for both Franco and English syntax")
        formatters.display_enhanced_ai_response(result, self.agent.current_model_id)
    
    async def _show_settings(self) -> None:
        """Show current settings."""
        agent_info = self.agent.get_agent_info()
        
        settings_text = (
            f"Model: {agent_info['current_model']}\n"
            f"Max Code Length: {agent_info['settings']['max_code_length']} lines\n"
            f"Execution Timeout: {agent_info['settings']['execution_timeout']} seconds\n"
            f"Model Cache Duration: {agent_info['settings']['model_cache_duration']} seconds\n"
            f"OpenRouter API Key: {'Set' if self.settings.openrouter.api_key else 'Not Set'}\n"
        )
        
        # Show cache info
        cache_info = self.model_manager.get_cache_info()
        settings_text += f"\nModel Cache: {'Valid' if cache_info.get('is_valid') else 'Invalid/Empty'}"
        
        formatters.display_message(settings_text, title="Settings")
    
    async def _clear_conversation(self) -> None:
        """Clear conversation history."""
        if Confirm.ask("🗑️ Clear conversation history?", default=False):
            self.conversation_history.clear()
            formatters.display_message("Conversation history cleared.", title="Success")
    
    async def _show_history(self) -> None:
        """Show conversation history."""
        if not self.conversation_history:
            formatters.display_message("No conversation history.", title="Info")
            return
        
        history_text = ""
        for i, entry in enumerate(self.conversation_history[-10:], 1):  # Show last 10
            role = "You" if entry['type'] == 'user' else "Assistant"
            content = entry['content'][:100] + "..." if len(entry['content']) > 100 else entry['content']
            history_text += f"{i}. {role}: {content}\n"
            
        formatters.display_message(history_text, title="Conversation History")
    
    async def _save_conversation(self) -> None:
        """Save conversation to file."""
        if not self.conversation_history:
            formatters.display_message("No conversation to save.", title="Info")
            return
        
        filename = Prompt.ask("Enter filename", default="flex_conversation.md")
        
        try:
            content = "# Flex AI Agent Conversation\n\n"
            for entry in self.conversation_history:
                role = "User" if entry['type'] == 'user' else "Assistant"
                content += f"## {role}\n\n{entry['content']}\n\n"
            
            with open(filename, 'w') as f:
                f.write(content)
            
            formatters.display_message(f"Conversation saved to {filename}", title="Success")
            
        except Exception as e:
            formatters.display_error(f"Failed to save conversation: {e}")
    
    async def _exit_command(self) -> None:
        """Exit the application."""
        self.console.print("👋 Goodbye!")
        self.is_running = False


async def main() -> None:
    """Main entry point for CLI."""
    cli = FlexCLI()
    await cli.start()


if __name__ == "__main__":
    asyncio.run(main())