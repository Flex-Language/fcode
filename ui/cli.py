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
            formatters.display_message("Goodbye!", title="Flex AI Agent")
        except Exception as e:
            formatters.display_error(f"Fatal error: {e}")
            sys.exit(1)
    
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
            f"Current model: [bold]{self.agent.current_model_id}[/bold]"
        )
        formatters.display_message(welcome_message, title="Flex AI Agent")
    
    async def _main_loop(self) -> None:
        """Main interaction loop."""
        while self.is_running:
            try:
                # Get user input
                user_input = Prompt.ask("You", console=self.console).strip()
                
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
                if Confirm.ask("\n🤔 Do you want to exit?", default=False):
                    break
                else:
                    formatters.display_message("Continuing...", title="Info")
            except Exception as e:
                formatters.display_error(f"Error: {e}")
    
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
        
        self.console.print("🤖 Assistant:", style="cyan", end=" ")
        
        try:
            # Stream response from agent
            response_content = ""
            last_content = ""
            
            async for chunk in self.agent.run_stream(user_input):
                # PydanticAI returns cumulative strings, so we need to extract only new content
                current_content = str(chunk)
                
                # Print only the new part
                if current_content.startswith(last_content):
                    new_part = current_content[len(last_content):]
                    if new_part:
                        self.console.print(new_part, end='', flush=True)
                    last_content = current_content
                    response_content = current_content
                else:
                    # This shouldn't happen with PydanticAI, but handle it just in case
                    self.console.print(current_content, end='', flush=True)
                    response_content += current_content
                    last_content += current_content
            
            # Add response to history
            self.conversation_history.append({
                'type': 'assistant',
                'content': response_content,
                'model': self.agent.current_model_id,
                'timestamp': asyncio.get_event_loop().time()
            })
            
            self.console.print()  # New line after response
            
        except Exception as e:
            formatters.display_error(f"Error processing request: {e}")
    
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
        self.console.print(result)
    
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
        self.is_running = False


async def main() -> None:
    """Main entry point for CLI."""
    cli = FlexCLI()
    await cli.start()


if __name__ == "__main__":
    asyncio.run(main())