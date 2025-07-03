import json
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

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
