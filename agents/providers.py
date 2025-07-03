"""
OpenRouter Provider Configuration for Flex AI Agent.

This module provides PydanticAI provider configuration for OpenRouter integration
with dynamic model selection and proper authentication handling.
"""

import os
from typing import Optional, Dict, Any, List
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from config.settings import Settings, get_settings
from agents.models import OpenRouterModel


class OpenRouterProviderManager:
    """Manages OpenRouter provider configurations and model creation."""
    
    def __init__(self, settings: Optional[Settings] = None):
        """Initialize provider manager with settings."""
        self.settings = settings or get_settings()
        self.current_provider = self._create_default_provider()
    
    def _create_default_provider(self) -> OpenAIProvider:
        """Create default OpenRouter provider."""
        return OpenAIProvider(
            api_key=self.settings.openrouter.api_key,
            base_url=self.settings.openrouter.base_url
        )
    
    def create_model(
        self, 
        model_id: str, 
        provider_config: Optional[Dict[str, Any]] = None
    ) -> OpenAIModel:
        """
        Create an OpenAI model configured for OpenRouter.
        
        Args:
            model_id: OpenRouter model ID (e.g., 'anthropic/claude-3.5-sonnet')
            provider_config: Optional provider-specific configuration
            
        Returns:
            Configured OpenAI model instance
        """
        # Create provider with optional custom config
        provider = self._create_provider_with_config(provider_config)
        
        # Create model with OpenRouter-specific settings
        model = OpenAIModel(
            model_id,
            provider=provider
        )
        
        return model
    
    def _create_provider_with_config(
        self, 
        provider_config: Optional[Dict[str, Any]] = None
    ) -> OpenAIProvider:
        """Create provider with custom configuration."""
        if not provider_config:
            return self.current_provider
        
        # Merge with default settings
        base_url = provider_config.get('base_url', self.settings.openrouter.base_url)
        api_key = provider_config.get('api_key', self.settings.openrouter.api_key)
        
        # Custom headers
        headers = {
            "HTTP-Referer": self.settings.openrouter.http_referer,
            "X-Title": self.settings.openrouter.app_title
        }
        
        if 'headers' in provider_config:
            headers.update(provider_config['headers'])
        
        return OpenAIProvider(
            base_url=base_url,
            api_key=api_key,
            default_headers=headers
        )
    
    def _get_openrouter_extra_body(
        self, 
        provider_config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Get OpenRouter-specific extra body parameters."""
        extra_body = {}
        
        if provider_config:
            # Provider-specific routing options
            if 'provider_routing' in provider_config:
                extra_body['provider'] = provider_config['provider_routing']
            
            # Cost optimization settings
            if 'cost_optimization' in provider_config:
                extra_body['cost_optimization'] = provider_config['cost_optimization']
            
            # Custom parameters
            if 'extra_body' in provider_config:
                extra_body.update(provider_config['extra_body'])
        
        return extra_body
    
    def create_agent(
        self, 
        model_id: str,
        system_prompt: str,
        deps_type: Optional[type] = None,
        result_type: Optional[type] = None,
        provider_config: Optional[Dict[str, Any]] = None
    ) -> Agent:
        """
        Create a PydanticAI agent with OpenRouter model.
        
        Args:
            model_id: OpenRouter model ID
            system_prompt: System prompt for the agent
            deps_type: Optional dependencies type
            result_type: Optional result type
            provider_config: Optional provider configuration
            
        Returns:
            Configured PydanticAI agent
        """
        model = self.create_model(model_id, provider_config)
        
        # Create agent with proper typing
        agent_kwargs = {
            'model': model,
            'system_prompt': system_prompt
        }
        
        if deps_type:
            agent_kwargs['deps_type'] = deps_type
        
        if result_type:
            agent_kwargs['result_type'] = result_type
        
        return Agent(**agent_kwargs)
    
    def update_model(self, agent: Agent, new_model_id: str) -> Agent:
        """
        Update an existing agent with a new model.
        
        Args:
            agent: Existing agent instance
            new_model_id: New OpenRouter model ID
            
        Returns:
            Agent with updated model
        """
        # Create new model
        new_model = self.create_model(new_model_id)
        
        # Update agent's model
        agent.model = new_model
        
        return agent
    
    def get_supported_models(self) -> List[str]:
        """
        Get list of supported OpenRouter model IDs.
        
        Returns:
            List of supported model IDs
        """
        # These are commonly available OpenRouter models
        # In a real implementation, this would query the OpenRouter API
        return [
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3.5-haiku",
            "anthropic/claude-3-opus",
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "openai/gpt-4-turbo",
            "openai/gpt-3.5-turbo",
            "meta-llama/llama-3.1-70b-instruct",
            "meta-llama/llama-3.1-8b-instruct",
            "google/gemini-pro",
            "google/gemini-pro-vision",
            "mistralai/mistral-7b-instruct",
            "mistralai/mixtral-8x7b-instruct",
            "cohere/command-r-plus",
            "cohere/command-r"
        ]
    
    def validate_model_id(self, model_id: str) -> bool:
        """
        Validate if a model ID is properly formatted.
        
        Args:
            model_id: Model ID to validate
            
        Returns:
            True if valid, False otherwise
        """
        # OpenRouter model IDs follow the pattern: provider/model
        if not model_id or '/' not in model_id:
            return False
        
        parts = model_id.split('/')
        if len(parts) != 2:
            return False
        
        provider, model = parts
        if not provider or not model:
            return False
        
        return True
    
    def get_model_info(self, model_id: str) -> Dict[str, Any]:
        """
        Get information about a specific model.
        
        Args:
            model_id: OpenRouter model ID
            
        Returns:
            Dictionary with model information
        """
        # This would typically query OpenRouter API for model details
        # For now, return basic information
        if not self.validate_model_id(model_id):
            raise ValueError(f"Invalid model ID: {model_id}")
        
        provider, model = model_id.split('/')
        
        return {
            "id": model_id,
            "provider": provider,
            "model": model,
            "supported": model_id in self.get_supported_models()
        }
    
    def create_fallback_chain(self, primary_model: str, fallback_models: List[str]) -> List[OpenAIModel]:
        """
        Create a chain of models for fallback support.
        
        Args:
            primary_model: Primary model ID
            fallback_models: List of fallback model IDs
            
        Returns:
            List of configured models
        """
        models = [self.create_model(primary_model)]
        
        for model_id in fallback_models:
            if self.validate_model_id(model_id):
                models.append(self.create_model(model_id))
        
        return models
    
    def get_cost_optimized_config(self, budget_limit: Optional[float] = None) -> Dict[str, Any]:
        """
        Get configuration optimized for cost efficiency.
        
        Args:
            budget_limit: Optional budget limit in USD
            
        Returns:
            Provider configuration for cost optimization
        """
        config = {
            'provider_routing': {
                'require_parameters': True,
                'data_collection': 'deny'  # Reduce costs by denying data collection
            },
            'cost_optimization': {
                'enable_fallbacks': True,
                'prefer_cheaper_models': True
            }
        }
        
        if budget_limit:
            config['cost_optimization']['budget_limit'] = budget_limit
        
        return config
    
    def get_performance_optimized_config(self) -> Dict[str, Any]:
        """
        Get configuration optimized for performance.
        
        Returns:
            Provider configuration for performance optimization
        """
        return {
            'provider_routing': {
                'require_parameters': True,
                'data_collection': 'allow'  # Allow data collection for better routing
            },
            'performance_optimization': {
                'enable_caching': True,
                'prefer_faster_models': True,
                'enable_streaming': True
            }
        }


# Global provider manager instance
provider_manager = OpenRouterProviderManager()


def create_flex_agent(
    model_id: str,
    system_prompt: str,
    deps_type: Optional[type] = None,
    result_type: Optional[type] = None,
    provider_config: Optional[Dict[str, Any]] = None
) -> Agent:
    """
    Convenience function to create a Flex AI agent with OpenRouter.
    
    Args:
        model_id: OpenRouter model ID
        system_prompt: System prompt
        deps_type: Optional dependencies type
        result_type: Optional result type
        provider_config: Optional provider configuration
        
    Returns:
        Configured PydanticAI agent
    """
    return provider_manager.create_agent(
        model_id=model_id,
        system_prompt=system_prompt,
        deps_type=deps_type,
        result_type=result_type,
        provider_config=provider_config
    )


def switch_model(agent: Agent, new_model_id: str) -> Agent:
    """
    Switch an agent to use a different model.
    
    Args:
        agent: Existing agent
        new_model_id: New model ID
        
    Returns:
        Agent with updated model
    """
    return provider_manager.update_model(agent, new_model_id)


def get_available_models() -> List[str]:
    """Get list of available OpenRouter models."""
    return provider_manager.get_supported_models()


def validate_model(model_id: str) -> bool:
    """Validate if a model ID is supported."""
    return provider_manager.validate_model_id(model_id)