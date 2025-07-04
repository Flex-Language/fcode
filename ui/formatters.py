import json
import re
import shutil
import textwrap
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from agents.models import OpenRouterModel, ModelSelection, CodeValidationResult, FlexExecutionResult as ExecutionResult

console = Console()

def display_code(code: str, language: str = "python"):
    """Displays syntax-highlighted code."""
    syntax = Syntax(code, language, theme="solarized-dark", line_numbers=True)
    console.print(syntax)

def display_model_list(models: list[OpenRouterModel]):
    """Displays a list of models in a table."""
    table = Table(title="Available Models")
    table.add_column("ID", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Context Length", style="green")
    table.add_column("Cost (Input)", style="yellow")
    table.add_column("Cost (Output)", style="yellow")

    for model in models:
        table.add_row(
            model.id,
            model.name,
            str(model.context_length),
            f"${model.pricing.prompt:.6f}" if model.pricing.prompt is not None else "N/A",
            f"${model.pricing.completion:.6f}" if model.pricing.completion is not None else "N/A",
        )
    console.print(table)

def display_model_selection(selection: ModelSelection):
    """Displays the selected model and reason."""
    if selection.model:
        panel = Panel(
            Text(f"Model: {selection.model.name}\nReason: {selection.reason}", justify="left"),
            title="Model Selection",
            border_style="green"
        )
        console.print(panel)

def display_validation_result(result: CodeValidationResult):
    """Displays the code validation result."""
    if result.is_valid:
        panel = Panel(
            Text("Code is valid and safe.", justify="center"),
            title="Validation Success",
            border_style="green"
        )
        console.print(panel)
    else:
        table = Table(title="Validation Errors")
        table.add_column("Error Type", style="red")
        table.add_column("Message", style="white")
        table.add_column("Line", style="cyan")

        for error in result.errors:
            table.add_row(error.error_type, error.message, str(error.line))
        console.print(table)

def display_execution_result(result: ExecutionResult):
    """Displays the code execution result."""
    if result.success:
        panel = Panel(
            Text(f"Exit Code: {result.exit_code}\n\nOutput:\n{result.stdout}", justify="left"),
            title="Execution Success",
            border_style="green"
        )
    else:
        panel = Panel(
            Text(f"Exit Code: {result.exit_code}\n\nError:\n{result.stderr}", justify="left"),
            title="Execution Failed",
            border_style="red"
        )
    console.print(panel)

def display_error(message: str):
    """Displays an error message."""
    panel = Panel(
        Text(message, justify="center"),
        title="Error",
        border_style="red"
    )
    console.print(panel)

def display_message(message: str, title: str = "Info"):
    """Displays a general message."""
    panel = Panel(
        Text(message, justify="center"),
        title=title,
        border_style="blue"
    )
    console.print(panel)


# Enhanced formatting functions inspired by the provided AI response formatting

def get_terminal_width():
    """Get the current terminal width with fallback for different environments."""
    try:
        # Try to get terminal size
        size = shutil.get_terminal_size()
        width = size.columns
        
        # Ensure minimum and maximum reasonable widths
        if width < 60:  # Minimum for readability
            return 60
        elif width > 120:  # Maximum for readability
            return 120
        else:
            return width
    except:
        # Fallback to 80 if terminal size detection fails
        return 80


def get_visible_length(text):
    """Get the visible length of text, excluding ANSI color codes."""
    if not text:
        return 0
    # Remove ANSI escape sequences to get actual visible length
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', text)
    return len(clean_text)


def pad_line_to_width(line, target_width, fill_char=' '):
    """Pad a line to exact target width, accounting for ANSI color codes."""
    visible_length = get_visible_length(line)
    if visible_length >= target_width:
        return line
    padding_needed = target_width - visible_length
    return line + (fill_char * padding_needed)


def wrap_text_responsive(text, width, indent=0):
    """Wrap text to specified width with optional indentation."""
    if not text:
        return [""]
    
    indent_str = " " * indent
    wrapper = textwrap.TextWrapper(
        width=width - indent,
        initial_indent=indent_str,
        subsequent_indent=indent_str,
        break_long_words=False,
        break_on_hyphens=False
    )
    
    # Handle multiple lines
    lines = text.split('\n')
    wrapped_lines = []
    
    for line in lines:
        if line.strip():
            wrapped_lines.extend(wrapper.wrap(line))
        else:
            wrapped_lines.append("")
    
    return wrapped_lines


def highlight_flex_syntax(code_line):
    """Apply syntax highlighting to Flex code while preserving indentation and spacing."""
    if not code_line:
        return code_line
    
    # Preserve leading whitespace
    leading_whitespace = code_line[:len(code_line) - len(code_line.lstrip())]
    content = code_line[len(leading_whitespace):]
    
    if not content.strip():  # If line is only whitespace
        return code_line
    
    # Create a list of tokens with their positions and types
    tokens = []
    i = 0
    line = content
    
    # Define token types and patterns
    franco_keywords = ['rakm', 'kasr', 'so2al', 'klma', 'dorg', 'sndo2', 'etb3', 'da5l', 'lw', 'aw', 'gher', 'karr', 'l7d', 'talama', 'rg3', 'w2f']
    english_keywords = ['int', 'float', 'bool', 'string', 'list', 'fun', 'print', 'scan', 'if', 'elif', 'else', 'for', 'while', 'return', 'break', 'func', 'main', 'println', 'readline', 'true', 'false', 'continue', 'to', 'var']
    all_keywords = franco_keywords + english_keywords
    
    # Process the line character by character
    result = ""
    i = 0
    while i < len(line):
        char = line[i]
        
        # Handle comments
        if char == '/' and i + 1 < len(line) and line[i + 1] == '/':
            # Everything from here to end of line is a comment
            result += f"[dim]{line[i:]}[/dim]"
            break
        
        # Handle strings
        elif char in ['"', "'"]:
            quote_char = char
            string_content = char
            i += 1
            while i < len(line) and line[i] != quote_char:
                string_content += line[i]
                i += 1
            if i < len(line):
                string_content += line[i]  # Add closing quote
            result += f"[yellow]{string_content}[/yellow]"
            i += 1
            continue
        
        # Handle numbers
        elif char.isdigit():
            number = ""
            while i < len(line) and (line[i].isdigit() or line[i] == '.'):
                number += line[i]
                i += 1
            result += f"[cyan]{number}[/cyan]"
            continue
        
        # Handle operators
        elif char in "=+-*/%<>!&|":
            # Check for multi-character operators
            if i + 1 < len(line):
                two_char = line[i:i+2]
                if two_char in ["==", "!=", "<=", ">=", "++", "--", "+=", "-=", "*=", "/=", "%=", "->", "&&", "||"]:
                    result += f"[red]{two_char}[/red]"
                    i += 2
                    continue
            result += f"[red]{char}[/red]"
            i += 1
            continue
        
        # Handle keywords
        elif char.isalpha() or char == '_':
            word = ""
            while i < len(line) and (line[i].isalnum() or line[i] == '_'):
                word += line[i]
                i += 1
            
            if word in all_keywords:
                result += f"[magenta]{word}[/magenta]"
            else:
                result += word
            continue
        
        # Handle everything else (whitespace, punctuation, etc.)
        else:
            result += char
            i += 1
    
    # Restore leading whitespace
    return leading_whitespace + result


def format_enhanced_ai_response(response, model_name=None):
    """
    Format the AI response with enhanced terminal UI including colors, sections, and better visual hierarchy.
    Now fully responsive and adaptive to terminal size.
    
    Args:
        response (str): The raw AI response
        model_name (str): The model name used (for display)
        
    Returns:
        str: Beautifully formatted response
    """
    if not response or len(response.strip()) == 0:
        return "[red]⚠ Empty response received[/red]"
    
    # Get dynamic terminal width
    terminal_width = get_terminal_width()
    content_width = terminal_width - 2  # Account for borders
    
    # Icons
    AI_ICON = "🤖"
    SUCCESS_ICON = "✅"
    ERROR_ICON = "❌"
    INFO_ICON = "💡"
    CODE_ICON = "📝"
    WARNING_ICON = "⚠️"
    FLEX_ICON = "🚀"
    
    formatted_output = []
    
    # Create responsive header
    header_text = f"{AI_ICON} FLEX AI ASSISTANT"
    if model_name:
        header_text += f" • {model_name}"
    
    # Use Rich Panel for the header
    header_panel = Panel(
        Text(header_text, justify="center", style="bold cyan"),
        border_style="cyan",
        padding=(0, 1)
    )
    formatted_output.append(header_panel)
    
    # Process response content
    lines = response.split('\n')
    current_section = []
    in_code_block = False
    code_language = ""
    
    for line in lines:
        # Detect code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                # End of code block - display the collected code
                code_content = '\n'.join(current_section)
                if code_content.strip():
                    # Use Rich Syntax for code highlighting
                    lang = code_language if code_language else "text"
                    if lang.lower() in ["flex", "franco"]:
                        # Apply custom Flex syntax highlighting
                        highlighted_lines = []
                        for code_line in current_section:
                            highlighted_lines.append(highlight_flex_syntax(code_line))
                        code_content = '\n'.join(highlighted_lines)
                        
                        # Use Text.from_markup to properly render Rich markup
                        code_panel = Panel(
                            Text.from_markup(code_content),
                            title=f"{CODE_ICON} Flex Code Example",
                            border_style="blue",
                            padding=(1, 2)
                        )
                    else:
                        # Use Rich syntax highlighting for other languages
                        syntax = Syntax(code_content, lang, theme="monokai", line_numbers=True)
                        code_panel = Panel(
                            syntax,
                            title=f"{CODE_ICON} Code Example ({lang})",
                            border_style="blue",
                            padding=(0, 1)
                        )
                    
                    formatted_output.append(code_panel)
                
                current_section = []
                in_code_block = False
                code_language = ""
            else:
                # Start of code block
                if current_section:
                    # Process previous text section
                    text_content = '\n'.join(current_section)
                    if text_content.strip():
                        formatted_output.append(format_text_section_rich(text_content))
                    current_section = []
                
                code_language = line.strip()[3:] or "text"
                in_code_block = True
            continue
        
        if in_code_block:
            current_section.append(line)
        else:
            current_section.append(line)
    
    # Process remaining section
    if current_section:
        if in_code_block:
            # Handle unclosed code block
            code_content = '\n'.join(current_section)
            if code_content.strip():
                lang = code_language if code_language else "text"
                if lang.lower() in ["flex", "franco"]:
                    # Apply custom Flex syntax highlighting
                    highlighted_lines = []
                    for code_line in current_section:
                        highlighted_lines.append(highlight_flex_syntax(code_line))
                    code_content = '\n'.join(highlighted_lines)
                    
                    # Use Text.from_markup to properly render Rich markup
                    code_panel = Panel(
                        Text.from_markup(code_content),
                        title=f"{CODE_ICON} Flex Code Example",
                        border_style="blue",
                        padding=(1, 2)
                    )
                else:
                    syntax = Syntax(code_content, lang, theme="monokai", line_numbers=True)
                    code_panel = Panel(
                        syntax,
                        title=f"{CODE_ICON} Code Example",
                        border_style="blue",
                        padding=(0, 1)
                    )
                
                formatted_output.append(code_panel)
        else:
            # Handle remaining text
            text_content = '\n'.join(current_section)
            if text_content.strip():
                formatted_output.append(format_text_section_rich(text_content))
    
    # Create responsive footer
    footer_text = f"{FLEX_ICON} Ready for your next question!"
    footer_panel = Panel(
        Text(footer_text, justify="center", style="bold green"),
        border_style="green",
        padding=(0, 1)
    )
    formatted_output.append(footer_panel)
    
    return formatted_output


def format_text_section_rich(text):
    """Format a text section with Rich styling and responsive text handling."""
    if not text.strip():
        return None
    
    # Process markdown-like formatting
    processed_text = text
    
    # Convert **bold** to Rich markup
    processed_text = re.sub(r'\*\*(.*?)\*\*', r'[bold]\1[/bold]', processed_text)
    
    # Convert *italic* to Rich markup
    processed_text = re.sub(r'\*(.*?)\*', r'[italic]\1[/italic]', processed_text)
    
    # Detect and style special sections
    lines = processed_text.split('\n')
    styled_lines = []
    
    for line in lines:
        stripped = line.strip()
        
        if not stripped:
            styled_lines.append("")
            continue
        
        # Headers (### or **)
        if stripped.startswith('###'):
            text_content = stripped[3:].strip()
            if any(keyword in text_content.lower() for keyword in ['solution', 'fix', 'correct']):
                styled_lines.append(f"[bold green]✅ {text_content}[/bold green]")
            elif any(keyword in text_content.lower() for keyword in ['error', 'problem', 'issue']):
                styled_lines.append(f"[bold red]❌ {text_content}[/bold red]")
            elif any(keyword in text_content.lower() for keyword in ['note', 'tip', 'remember']):
                styled_lines.append(f"[bold yellow]💡 {text_content}[/bold yellow]")
            else:
                styled_lines.append(f"[bold cyan]📋 {text_content}[/bold cyan]")
        
        # Bullet points
        elif stripped.startswith('- ') or stripped.startswith('• '):
            text_content = stripped[2:]
            styled_lines.append(f"[blue]  • {text_content}[/blue]")
        
        # Numbered lists
        elif len(stripped) > 2 and stripped[0].isdigit() and stripped[1] == '.':
            styled_lines.append(f"[blue]{stripped}[/blue]")
        
        # Special keywords
        elif any(keyword in stripped.lower() for keyword in ['error', 'problem', 'issue', 'wrong']):
            styled_lines.append(f"[red]⚠️ {stripped}[/red]")
        elif any(keyword in stripped.lower() for keyword in ['fix', 'solution', 'correct']):
            styled_lines.append(f"[green]✅ {stripped}[/green]")
        elif any(keyword in stripped.lower() for keyword in ['note', 'tip', 'remember']):
            styled_lines.append(f"[yellow]💡 {stripped}[/yellow]")
        else:
            styled_lines.append(stripped)
    
    formatted_content = '\n'.join(styled_lines)
    
    # Create a panel for the text content
    return Panel(
        Text.from_markup(formatted_content),
        border_style="white",
        padding=(1, 2)
    )


def display_enhanced_ai_response(response, model_name=None):
    """Display an AI response with enhanced formatting."""
    formatted_panels = format_enhanced_ai_response(response, model_name)
    
    if isinstance(formatted_panels, list):
        for panel in formatted_panels:
            if panel:  # Skip None panels
                console.print(panel)
                console.print()  # Add spacing between panels
    else:
        console.print(formatted_panels)
