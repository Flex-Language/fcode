"""
OpenRouter Model Manager for Flex AI Agent.

This module provides comprehensive model management functionality including:
- Model listing with caching
- Model filtering and searching
- OpenRouter API authentication
- Error handling and retries
- Performance metrics tracking
"""

import asyncio
import json
import httpx
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config'))

from agents.models import (
    OpenRouterModel,
    ModelFilter,
    ModelSelection,
    ModelMetrics
)
from config.settings import Settings


class ModelManagerError(Exception):
    """Custom exception for model manager errors."""
    pass


class ModelManager:
    """Manages OpenRouter models with caching and filtering capabilities."""
    
    def __init__(self, settings: Settings):
        """Initialize ModelManager with configuration."""
        self.settings = settings
        self.api_key = settings.openrouter.api_key
        self.base_url = settings.openrouter.base_url
        self.http_referer = settings.openrouter.http_referer
        self.app_title = settings.openrouter.app_title
        self.cache_duration = timedelta(seconds=settings.app.model_cache_duration)
        
        # Cache configuration
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "models_cache.json"
        
        # Performance metrics
        self.metrics: Dict[str, ModelMetrics] = {}
        
        # HTTP client configuration
        self.timeout = httpx.Timeout(30.0)
        self.retry_attempts = 3
        self.retry_delay = 1.0
    
    async def list_models(self, use_cache: bool = True) -> List[OpenRouterModel]:
        """
        List all available OpenRouter models.
        
        Args:
            use_cache: Whether to use cached results
            
        Returns:
            List of OpenRouter models
            
        Raises:
            ModelManagerError: If API request fails
        """
        # Check cache first
        if use_cache and self._is_cache_valid():
            cached_models = self._load_from_cache()
            if cached_models:
                return cached_models
        
        # Fetch from API with retry logic
        for attempt in range(self.retry_attempts):
            try:
                models = await self._fetch_models_from_api()
                
                # Cache the results
                self._save_to_cache(models)
                
                return models
                
            except httpx.HTTPError as e:
                if attempt == self.retry_attempts - 1:
                    raise ModelManagerError(f"Failed to fetch models after {self.retry_attempts} attempts: {e}")
                
                # Exponential backoff
                await asyncio.sleep(self.retry_delay * (2 ** attempt))
        
        # This should never be reached, but just in case
        raise ModelManagerError("Unexpected error in model fetching")
    
    async def _fetch_models_from_api(self) -> List[OpenRouterModel]:
        """Fetch models from OpenRouter API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": self.http_referer,
            "X-Title": self.app_title,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(
                f"{self.base_url}/models",
                headers=headers
            )
            
            # Reason: Check status code explicitly for better error handling
            if response.status_code == 401:
                raise ModelManagerError("Invalid OpenRouter API key")
            elif response.status_code == 429:
                raise ModelManagerError("Rate limit exceeded")
            elif response.status_code != 200:
                raise ModelManagerError(f"API request failed with status {response.status_code}")
            
            try:
                data = response.json()
            except json.JSONDecodeError:
                raise ModelManagerError("Invalid JSON response from API")
            
            # Parse and validate models
            models = []
            for model_data in data.get("data", []):
                try:
                    # Ensure required fields exist with defaults
                    model_info = {
                        "id": model_data.get("id", ""),
                        "name": model_data.get("name", "Unknown"),
                        "description": model_data.get("description"),
                        "pricing": model_data.get("pricing", {"prompt": 0, "completion": 0}),
                        "context_length": model_data.get("context_length", 0),
                        "architecture": model_data.get("architecture"),
                        "top_provider": model_data.get("top_provider"),
                        "per_request_limits": model_data.get("per_request_limits"),
                        "supports_tools": model_data.get("supports_tools", False),
                        "supports_streaming": model_data.get("supports_streaming", False)
                    }
                    
                    # Skip invalid models
                    if not model_info["id"] or "/" not in model_info["id"]:
                        continue
                    
                    model = OpenRouterModel(**model_info)
                    models.append(model)
                    
                except Exception as e:
                    # Log but don't fail - skip invalid models
                    print(f"Warning: Skipping invalid model {model_data.get('id', 'unknown')}: {e}")
                    continue
            
            return models
    
    async def filter_models(self, filters: ModelFilter) -> List[OpenRouterModel]:
        """
        Filter models based on criteria.
        
        Args:
            filters: Filtering criteria
            
        Returns:
            List of filtered models
        """
        models = await self.list_models()
        filtered = []
        
        for model in models:
            if self._matches_filter(model, filters):
                filtered.append(model)
        
        return filtered
    
    def _matches_filter(self, model: OpenRouterModel, filters: ModelFilter) -> bool:
        """Check if model matches filter criteria."""
        # Search term filter
        if filters.search_term:
            search_lower = filters.search_term.lower()
            if not (
                search_lower in model.name.lower() or
                search_lower in model.id.lower() or
                (model.description and search_lower in model.description.lower())
            ):
                return False
        
        # Price filters
        if filters.max_price_prompt is not None:
            prompt_price = model.pricing.get("prompt", float('inf'))
            if prompt_price > filters.max_price_prompt:
                return False
        
        if filters.max_price_completion is not None:
            completion_price = model.pricing.get("completion", float('inf'))
            if completion_price > filters.max_price_completion:
                return False
        
        # Context length filter
        if filters.min_context_length is not None:
            if model.context_length < filters.min_context_length:
                return False
        
        # Provider filter
        if filters.provider is not None:
            if not model.top_provider or filters.provider.lower() not in model.top_provider.lower():
                return False
        
        # Architecture filter
        if filters.architecture is not None:
            if not model.architecture or filters.architecture.lower() not in model.architecture.lower():
                return False
        
        # Feature filters
        if filters.supports_tools is not None:
            if model.supports_tools != filters.supports_tools:
                return False
        
        if filters.supports_streaming is not None:
            if model.supports_streaming != filters.supports_streaming:
                return False
        
        # Free models only filter
        if filters.free_models_only:
            prompt_price = model.pricing.get("prompt", 0)
            completion_price = model.pricing.get("completion", 0)
            if prompt_price > 0 or completion_price > 0:
                return False
        
        return True
    
    async def get_model_by_id(self, model_id: str) -> Optional[OpenRouterModel]:
        """
        Get a specific model by ID.
        
        Args:
            model_id: Model identifier
            
        Returns:
            OpenRouter model or None if not found
        """
        models = await self.list_models()
        for model in models:
            if model.id == model_id:
                return model
        return None
    
    async def suggest_models(
        self, 
        task_description: str, 
        max_suggestions: int = 5
    ) -> List[ModelSelection]:
        """
        Suggest models based on task description.
        
        Args:
            task_description: Description of the task
            max_suggestions: Maximum number of suggestions
            
        Returns:
            List of model selections with reasons
        """
        models = await self.list_models()
        suggestions = []
        
        # Reason: Simple heuristic-based model suggestion
        # Could be enhanced with ML-based recommendations
        
        # Prefer models with lower cost for simple tasks
        simple_keywords = ["hello", "simple", "basic", "test"]
        is_simple_task = any(keyword in task_description.lower() for keyword in simple_keywords)
        
        # Prefer models with tool support for complex tasks
        complex_keywords = ["complex", "function", "tool", "api", "integration"]
        needs_tools = any(keyword in task_description.lower() for keyword in complex_keywords)
        
        # Score models based on task requirements
        for model in models:
            score = 0
            reason_parts = []
            
            # Cost considerations
            prompt_price = model.pricing.get("prompt", 0)
            if is_simple_task and prompt_price < 0.00001:
                score += 3
                reason_parts.append("cost-effective for simple tasks")
            elif not is_simple_task and prompt_price < 0.0001:
                score += 2
                reason_parts.append("good value for complex tasks")
            
            # Tool support
            if needs_tools and model.supports_tools:
                score += 2
                reason_parts.append("supports function calling")
            
            # Context length
            if model.context_length > 100000:
                score += 1
                reason_parts.append("large context window")
            
            # Popular models (heuristic based on name)
            if any(popular in model.name.lower() for popular in ["claude", "gpt", "llama"]):
                score += 1
                reason_parts.append("popular and reliable")
            
            if score > 0:
                reason = "Recommended because: " + ", ".join(reason_parts)
                suggestions.append(ModelSelection(
                    model=model,
                    reason=reason,
                    cost_estimate=self._estimate_cost(model, task_description)
                ))
        
        # Sort by score and return top suggestions
        suggestions.sort(key=lambda x: x.cost_estimate or float('inf'))
        return suggestions[:max_suggestions]
    
    def _estimate_cost(self, model: OpenRouterModel, task_description: str) -> float:
        """Estimate cost for a task with given model."""
        # Simple cost estimation based on task description length
        # This is a rough approximation - actual cost depends on model response
        estimated_prompt_tokens = len(task_description.split()) * 1.3  # ~1.3 tokens per word
        estimated_completion_tokens = estimated_prompt_tokens * 0.5  # Assume 50% of prompt length
        
        prompt_price = model.pricing.get("prompt", 0)
        completion_price = model.pricing.get("completion", 0)
        
        total_cost = (
            estimated_prompt_tokens * prompt_price +
            estimated_completion_tokens * completion_price
        )
        
        return total_cost
    
    def _is_cache_valid(self) -> bool:
        """Check if cache is still valid."""
        if not self.cache_file.exists():
            return False
        
        cache_time = datetime.fromtimestamp(self.cache_file.stat().st_mtime)
        return datetime.now() - cache_time < self.cache_duration
    
    def _load_from_cache(self) -> List[OpenRouterModel]:
        """Load models from cache."""
        try:
            with open(self.cache_file, 'r') as f:
                data = json.load(f)
                return [OpenRouterModel(**model_data) for model_data in data]
        except Exception as e:
            print(f"Warning: Failed to load cache: {e}")
            return []
    
    def _save_to_cache(self, models: List[OpenRouterModel]) -> None:
        """Save models to cache."""
        try:
            with open(self.cache_file, 'w') as f:
                json.dump(
                    [model.dict() for model in models],
                    f,
                    indent=2,
                    default=str
                )
        except Exception as e:
            print(f"Warning: Failed to save cache: {e}")
    
    def clear_cache(self) -> None:
        """Clear the model cache."""
        if self.cache_file.exists():
            self.cache_file.unlink()
    
    def get_cache_info(self) -> Dict[str, Any]:
        """Get cache information."""
        if not self.cache_file.exists():
            return {"exists": False}
        
        stat = self.cache_file.stat()
        return {
            "exists": True,
            "size": stat.st_size,
            "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "is_valid": self._is_cache_valid()
        }
    
    def update_metrics(self, model_id: str, success: bool, response_time: float, tokens_used: int = 0, cost: float = 0.0) -> None:
        """Update performance metrics for a model."""
        if model_id not in self.metrics:
            self.metrics[model_id] = ModelMetrics(model_id=model_id)
        
        metrics = self.metrics[model_id]
        metrics.total_requests += 1
        
        if success:
            metrics.successful_requests += 1
        else:
            metrics.failed_requests += 1
        
        # Update average response time
        total_time = metrics.average_response_time * (metrics.total_requests - 1) + response_time
        metrics.average_response_time = total_time / metrics.total_requests
        
        metrics.total_tokens_used += tokens_used
        metrics.total_cost += cost
        metrics.last_used = datetime.now()
    
    def get_metrics(self, model_id: Optional[str] = None) -> Dict[str, ModelMetrics]:
        """Get performance metrics."""
        if model_id:
            return {model_id: self.metrics.get(model_id)}
        return self.metrics.copy()