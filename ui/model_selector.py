"""
Interactive Model Selection UI for Flex AI Agent.

This module provides an interactive CLI interface for browsing, filtering,
and selecting OpenRouter models using the inquirer library.
"""

import asyncio
from typing import List, Optional, Dict, Any, Tuple
import inquirer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from agents.models import OpenRouterModel, ModelFilter
from tools.model_manager import ModelManager
from config.settings import Settings, get_settings


class ModelSelector:
    """Interactive model selection interface."""
    
    def __init__(self, model_manager: ModelManager, settings: Optional[Settings] = None):
        """Initialize model selector."""
        self.model_manager = model_manager
        self.settings = settings or get_settings()
        self.console = Console()
        
        # Cache for models to avoid repeated API calls
        self._model_cache: Optional[List[OpenRouterModel]] = None
        
        # Display settings
        self.models_per_page = 20
        self.max_description_length = 80
    
    async def select_model_interactive(
        self, 
        current_model: Optional[str] = None,
        filter_criteria: Optional[ModelFilter] = None
    ) -> Optional[str]:
        """
        Interactive model selection with filtering and pagination.
        
        Args:
            current_model: Currently selected model ID
            filter_criteria: Optional initial filter criteria
            
        Returns:
            Selected model ID or None if cancelled
        """
        try:
            while True:
                # Main menu
                action = await self._show_main_menu(current_model)
                
                if action == "browse":
                    result = await self._browse_models(current_model, filter_criteria)
                    if result:
                        return result
                
                elif action == "search":
                    result = await self._search_models(current_model)
                    if result:
                        return result
                
                elif action == "filter":
                    filter_criteria = await self._setup_filters()
                    # Continue to show filtered results
                    result = await self._browse_models(current_model, filter_criteria)
                    if result:
                        return result
                
                elif action == "favorites":
                    result = await self._show_favorite_models(current_model)
                    if result:
                        return result
                
                elif action == "details":
                    await self._show_model_details(current_model)
                
                elif action == "refresh":
                    await self._refresh_model_cache()
                    self.console.print("✅ Model cache refreshed!", style="green")
                
                elif action == "exit":
                    return None
                
        except KeyboardInterrupt:
            self.console.print("\n👋 Model selection cancelled.", style="yellow")
            return None
    
    async def _show_main_menu(self, current_model: Optional[str]) -> str:
        """Show the main model selection menu."""
        self.console.clear()
        
        # Show header
        header = Text("🤖 Flex AI Agent - Model Selection", style="bold blue")
        if current_model:
            header.append(f"\nCurrent: {current_model}", style="cyan")
        
        self.console.print(Panel(header, title="Model Selector"))
        
        # Menu options
        choices = [
            ("Browse all models", "browse"),
            ("Search models", "search"),
            ("Filter models", "filter"),
            ("Show favorite models", "favorites"),
            ("Show current model details", "details") if current_model else None,
            ("Refresh model cache", "refresh"),
            ("Exit", "exit")
        ]
        
        # Remove None choices
        choices = [choice for choice in choices if choice is not None]
        
        questions = [
            inquirer.List(
                'action',
                message="Select an action",
                choices=choices,
                carousel=True
            )
        ]
        
        answers = inquirer.prompt(questions)
        return answers['action'] if answers else 'exit'
    
    async def _browse_models(
        self, 
        current_model: Optional[str],
        filter_criteria: Optional[ModelFilter] = None
    ) -> Optional[str]:
        """Browse models with pagination."""
        # Get models
        if filter_criteria:
            models = await self.model_manager.filter_models(filter_criteria)
        else:
            models = await self._get_cached_models()
        
        if not models:
            self.console.print("❌ No models found.", style="red")
            input("\nPress Enter to continue...")
            return None
        
        # Sort models by name
        models.sort(key=lambda m: m.name)
        
        # Paginate models
        page = 0
        total_pages = (len(models) - 1) // self.models_per_page + 1
        
        while True:
            start_idx = page * self.models_per_page
            end_idx = min(start_idx + self.models_per_page, len(models))
            page_models = models[start_idx:end_idx]
            
            # Display page
            self.console.clear()
            self._display_models_table(page_models, current_model, page + 1, total_pages)
            
            # Create choices for this page
            choices = []
            for i, model in enumerate(page_models):
                label = self._format_model_choice(model, current_model)
                choices.append((label, model.id))
            
            # Add navigation options
            choices.append(("──────────────────", None))
            
            if page > 0:
                choices.append(("◀ Previous page", "prev"))
            if page < total_pages - 1:
                choices.append(("Next page ▶", "next"))
            
            choices.extend([
                ("🔍 Show model details", "details"),
                ("↩ Back to main menu", "back")
            ])
            
            questions = [
                inquirer.List(
                    'choice',
                    message=f"Select a model (Page {page + 1}/{total_pages})",
                    choices=choices,
                    carousel=True
                )
            ]
            
            answers = inquirer.prompt(questions)
            if not answers:
                return None
            
            choice = answers['choice']
            
            if choice == "prev":
                page = max(0, page - 1)
            elif choice == "next":
                page = min(total_pages - 1, page + 1)
            elif choice == "details":
                model_id = await self._select_model_for_details(page_models)
                if model_id:
                    await self._show_model_details(model_id)
            elif choice == "back":
                return None
            elif choice and choice != "separator":
                # Model selected
                return choice
    
    async def _search_models(self, current_model: Optional[str]) -> Optional[str]:
        """Search models by name or description."""
        questions = [
            inquirer.Text(
                'search_term',
                message="Enter search term (name, provider, or description)"
            )
        ]
        
        answers = inquirer.prompt(questions)
        if not answers or not answers['search_term']:
            return None
        
        search_term = answers['search_term'].strip()
        
        # Create filter with search term
        filter_criteria = ModelFilter(search_term=search_term)
        
        # Browse filtered results
        return await self._browse_models(current_model, filter_criteria)
    
    async def _setup_filters(self) -> ModelFilter:
        """Set up model filtering criteria."""
        self.console.print("🔧 Model Filtering Options", style="bold blue")
        
        questions = [
            inquirer.Text(
                'search_term',
                message="Search term (optional)"
            ),
            inquirer.Text(
                'max_price_prompt',
                message="Max price per prompt token (optional, e.g., 0.00001)"
            ),
            inquirer.Text(
                'min_context_length',
                message="Minimum context length (optional, e.g., 100000)"
            ),
            inquirer.Text(
                'provider',
                message="Provider filter (optional, e.g., anthropic, openai)"
            ),
            inquirer.Checkbox(
                'features',
                message="Required features",
                choices=[
                    ('Function calling support', 'tools'),
                    ('Streaming support', 'streaming'),
                    ('Free models only', 'free_only')
                ]
            )
        ]
        
        answers = inquirer.prompt(questions)
        if not answers:
            return ModelFilter()
        
        # Parse answers
        filter_kwargs = {}
        
        if answers.get('search_term'):
            filter_kwargs['search_term'] = answers['search_term']
        
        if answers.get('max_price_prompt'):
            try:
                filter_kwargs['max_price_prompt'] = float(answers['max_price_prompt'])
            except ValueError:
                pass
        
        if answers.get('min_context_length'):
            try:
                filter_kwargs['min_context_length'] = int(answers['min_context_length'])
            except ValueError:
                pass
        
        if answers.get('provider'):
            filter_kwargs['provider'] = answers['provider']
        
        features = answers.get('features', [])
        if 'tools' in features:
            filter_kwargs['supports_tools'] = True
        if 'streaming' in features:
            filter_kwargs['supports_streaming'] = True
        if 'free_only' in features:
            filter_kwargs['free_models_only'] = True
        
        return ModelFilter(**filter_kwargs)
    
    async def _show_favorite_models(self, current_model: Optional[str]) -> Optional[str]:
        """Show a curated list of recommended models."""
        # Get suggested models for Flex programming
        suggested = await self.model_manager.suggest_models(
            "Flex programming language code generation and assistance",
            max_suggestions=10
        )
        
        if not suggested:
            self.console.print("❌ No model suggestions available.", style="red")
            input("\nPress Enter to continue...")
            return None
        
        self.console.clear()
        self.console.print("⭐ Recommended Models for Flex Programming", style="bold green")
        
        # Create choices
        choices = []
        for selection in suggested:
            model = selection.model
            label = f"{model.name}"
            
            # Add cost estimate
            if selection.cost_estimate:
                label += f" (${selection.cost_estimate:.6f}/request)"
            
            # Add reason
            label += f"\n   💡 {selection.reason}"
            
            choices.append((label, model.id))
        
        choices.append(("↩ Back to main menu", "back"))
        
        questions = [
            inquirer.List(
                'choice',
                message="Select a recommended model",
                choices=choices,
                carousel=True
            )
        ]
        
        answers = inquirer.prompt(questions)
        if not answers or answers['choice'] == 'back':
            return None
        
        return answers['choice']
    
    async def _show_model_details(self, model_id: str) -> None:
        """Show detailed information about a model."""
        if not model_id:
            return
        
        model = await self.model_manager.get_model_by_id(model_id)
        if not model:
            self.console.print(f"❌ Model '{model_id}' not found.", style="red")
            input("\nPress Enter to continue...")
            return
        
        self.console.clear()
        
        # Create detailed info panel
        details = Text()
        details.append(f"Model: {model.name}\n", style="bold blue")
        details.append(f"ID: {model.id}\n")
        details.append(f"Provider: {model.top_provider or 'Unknown'}\n")
        details.append(f"Architecture: {model.architecture or 'Unknown'}\n")
        details.append(f"Context Length: {model.context_length:,} tokens\n")
        
        # Pricing
        prompt_price = model.pricing.get('prompt', 0)
        completion_price = model.pricing.get('completion', 0)
        details.append(f"Pricing:\n")
        details.append(f"  • Prompt: ${prompt_price:.8f} per token\n")
        details.append(f"  • Completion: ${completion_price:.8f} per token\n")
        
        # Features
        features = []
        if model.supports_tools:
            features.append("Function calling")
        if model.supports_streaming:
            features.append("Streaming")
        
        if features:
            details.append(f"Features: {', '.join(features)}\n")
        
        # Description
        if model.description:
            description = model.description
            if len(description) > 200:
                description = description[:200] + "..."
            details.append(f"\nDescription:\n{description}")
        
        self.console.print(Panel(details, title=f"Model Details: {model.name}"))
        
        input("\nPress Enter to continue...")
    
    async def _select_model_for_details(self, models: List[OpenRouterModel]) -> Optional[str]:
        """Select a model to show details for."""
        choices = [(self._format_model_choice(model, None), model.id) for model in models]
        choices.append(("Cancel", None))
        
        questions = [
            inquirer.List(
                'model_id',
                message="Select model to view details",
                choices=choices,
                carousel=True
            )
        ]
        
        answers = inquirer.prompt(questions)
        return answers.get('model_id') if answers else None
    
    def _display_models_table(
        self, 
        models: List[OpenRouterModel], 
        current_model: Optional[str],
        page: int,
        total_pages: int
    ) -> None:
        """Display models in a formatted table."""
        table = Table(title=f"Available Models (Page {page}/{total_pages})")
        
        table.add_column("Name", style="cyan")
        table.add_column("Provider", style="green")
        table.add_column("Context", justify="right", style="yellow")
        table.add_column("Price/1K", justify="right", style="magenta")
        table.add_column("Features", style="blue")
        table.add_column("Current", justify="center", style="red")
        
        for model in models:
            # Calculate price per 1K tokens
            prompt_price_1k = model.pricing.get('prompt', 0) * 1000
            completion_price_1k = model.pricing.get('completion', 0) * 1000
            price_str = f"${prompt_price_1k:.3f}/${completion_price_1k:.3f}"
            
            # Features
            features = []
            if model.supports_tools:
                features.append("🔧")
            if model.supports_streaming:
                features.append("📡")
            feature_str = "".join(features) or "—"
            
            # Current indicator
            current_indicator = "●" if model.id == current_model else ""
            
            # Provider (extract from ID)
            provider = model.id.split('/')[0] if '/' in model.id else "Unknown"
            
            table.add_row(
                model.name[:30] + ("..." if len(model.name) > 30 else ""),
                provider,
                f"{model.context_length // 1000}K",
                price_str,
                feature_str,
                current_indicator
            )
        
        self.console.print(table)
    
    def _format_model_choice(self, model: OpenRouterModel, current_model: Optional[str]) -> str:
        """Format a model for display in choice list."""
        name = model.name
        if len(name) > 40:
            name = name[:37] + "..."
        
        # Add pricing info
        prompt_price = model.pricing.get('prompt', 0) * 1000  # Per 1K tokens
        completion_price = model.pricing.get('completion', 0) * 1000
        
        choice = f"{name}"
        
        if prompt_price > 0 or completion_price > 0:
            choice += f" (${prompt_price:.2f}/${completion_price:.2f} per 1K)"
        else:
            choice += " (Free)"
        
        # Add context length
        choice += f" [{model.context_length // 1000}K ctx]"
        
        # Mark current model
        if model.id == current_model:
            choice = "● " + choice + " (CURRENT)"
        
        return choice
    
    async def _get_cached_models(self) -> List[OpenRouterModel]:
        """Get models from cache or fetch if not cached."""
        if self._model_cache is None:
            self.console.print("📡 Loading models from OpenRouter...", style="yellow")
            self._model_cache = await self.model_manager.list_models()
        
        return self._model_cache
    
    async def _refresh_model_cache(self) -> None:
        """Refresh the model cache."""
        self.console.print("🔄 Refreshing model cache...", style="yellow")
        self._model_cache = await self.model_manager.list_models(use_cache=False)
    
    def quick_select(self, models: List[str], current_model: Optional[str] = None) -> Optional[str]:
        """Quick model selection from a predefined list."""
        if not models:
            return None
        
        choices = []
        for model_id in models:
            label = model_id
            if model_id == current_model:
                label += " (CURRENT)"
            choices.append((label, model_id))
        
        choices.append(("Cancel", None))
        
        questions = [
            inquirer.List(
                'model_id',
                message="Select a model",
                choices=choices,
                carousel=True
            )
        ]
        
        answers = inquirer.prompt(questions)
        return answers.get('model_id') if answers else None