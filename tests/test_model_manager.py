"""
Unit tests for OpenRouter Model Manager.

These tests validate the model management functionality including
API integration, caching, filtering, and error handling.
"""

import pytest
import asyncio
import json
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import httpx

from tools.model_manager import ModelManager, ModelManagerError
from agents.models import OpenRouterModel, ModelFilter
from config.settings import Settings, OpenRouterSettings, FlexSettings, ApplicationSettings


class TestModelManager:
    """Test suite for ModelManager."""
    
    @pytest.fixture
    def mock_settings(self):
        """Create mock settings for testing."""
        return Settings(
            openrouter=OpenRouterSettings(
                api_key="test_api_key",
                base_url="https://test.openrouter.ai/api/v1",
                http_referer="https://test.github.com",
                app_title="Test App"
            ),
            flex=FlexSettings(),
            app=ApplicationSettings(model_cache_duration=3600)
        )
    
    @pytest.fixture
    def manager(self, mock_settings):
        """Create ModelManager instance for testing."""
        return ModelManager(mock_settings)
    
    @pytest.fixture
    def sample_models(self):
        """Sample model data for testing."""
        return [
            {
                "id": "anthropic/claude-3-5-sonnet",
                "name": "Claude 3.5 Sonnet",
                "description": "Advanced AI model",
                "pricing": {"prompt": 0.000015, "completion": 0.000075},
                "context_length": 200000,
                "architecture": {"modality": "text->text", "instruct_type": "claude"},
                "top_provider": {"context_length": 200000, "is_moderated": False},
                "supports_tools": True,
                "supports_streaming": True
            },
            {
                "id": "openai/gpt-4o",
                "name": "GPT-4o",
                "description": "OpenAI's flagship model",
                "pricing": {"prompt": 0.00005, "completion": 0.00015},
                "context_length": 128000,
                "architecture": {"modality": "text->text", "instruct_type": "openai"},
                "top_provider": {"context_length": 128000, "is_moderated": False},
                "supports_tools": True,
                "supports_streaming": True
            },
            {
                "id": "meta-llama/llama-3-8b-instruct",
                "name": "Llama 3 8B Instruct",
                "description": "Meta's open source model",
                "pricing": {"prompt": 0.0, "completion": 0.0},
                "context_length": 8000,
                "architecture": {"modality": "text->text", "instruct_type": "llama"},
                "top_provider": {"context_length": 8000, "is_moderated": False},
                "supports_tools": False,
                "supports_streaming": True
            }
        ]
    
    @pytest.mark.asyncio
    async def test_fetch_models_from_api_success(self, manager, sample_models):
        """Test successful model fetching from API."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": sample_models}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            models = await manager._fetch_models_from_api()
            
            assert len(models) == 3
            assert models[0].id == "anthropic/claude-3-5-sonnet"
            assert models[0].name == "Claude 3.5 Sonnet"
            assert models[0].supports_tools == True
    
    @pytest.mark.asyncio
    async def test_fetch_models_from_api_auth_error(self, manager):
        """Test API authentication error handling."""
        mock_response = Mock()
        mock_response.status_code = 401
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            with pytest.raises(ModelManagerError) as exc_info:
                await manager._fetch_models_from_api()
            
            assert "Invalid OpenRouter API key" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_fetch_models_from_api_rate_limit(self, manager):
        """Test API rate limit error handling."""
        mock_response = Mock()
        mock_response.status_code = 429
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            
            with pytest.raises(ModelManagerError) as exc_info:
                await manager._fetch_models_from_api()
            
            assert "Rate limit exceeded" in str(exc_info.value)
    
    @pytest.mark.asyncio
    async def test_list_models_with_cache(self, manager, sample_models):
        """Test model listing with cache functionality."""
        # Mock cache as valid
        with patch.object(manager, '_is_cache_valid', return_value=True):
            with patch.object(manager, '_load_from_cache', return_value=[
                OpenRouterModel(**model) for model in sample_models
            ]):
                models = await manager.list_models(use_cache=True)
                
                assert len(models) == 3
                assert models[0].id == "anthropic/claude-3-5-sonnet"
    
    @pytest.mark.asyncio
    async def test_list_models_without_cache(self, manager, sample_models):
        """Test model listing without cache."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": sample_models}
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response
            with patch.object(manager, '_save_to_cache') as mock_save:
                
                models = await manager.list_models(use_cache=False)
                
                assert len(models) == 3
                mock_save.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_filter_models_by_price(self, manager, sample_models):
        """Test model filtering by price."""
        # Setup models
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            # Filter for free models only
            filter_criteria = ModelFilter(free_models_only=True)
            filtered = await manager.filter_models(filter_criteria)
            
            assert len(filtered) == 1
            assert filtered[0].id == "meta-llama/llama-3-8b-instruct"
    
    @pytest.mark.asyncio
    async def test_filter_models_by_search_term(self, manager, sample_models):
        """Test model filtering by search term."""
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            # Search for "claude"
            filter_criteria = ModelFilter(search_term="claude")
            filtered = await manager.filter_models(filter_criteria)
            
            assert len(filtered) == 1
            assert "claude" in filtered[0].name.lower()
    
    @pytest.mark.asyncio
    async def test_filter_models_by_context_length(self, manager, sample_models):
        """Test model filtering by context length."""
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            # Filter for models with at least 100k context
            filter_criteria = ModelFilter(min_context_length=100000)
            filtered = await manager.filter_models(filter_criteria)
            
            assert len(filtered) == 2  # Claude and GPT-4o
            assert all(m.context_length >= 100000 for m in filtered)
    
    @pytest.mark.asyncio
    async def test_filter_models_by_features(self, manager, sample_models):
        """Test model filtering by feature support."""
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            # Filter for models that support tools
            filter_criteria = ModelFilter(supports_tools=True)
            filtered = await manager.filter_models(filter_criteria)
            
            assert len(filtered) == 2  # Claude and GPT-4o
            assert all(m.supports_tools for m in filtered)
    
    @pytest.mark.asyncio
    async def test_get_model_by_id_found(self, manager, sample_models):
        """Test getting a specific model by ID."""
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            model = await manager.get_model_by_id("anthropic/claude-3-5-sonnet")
            
            assert model is not None
            assert model.id == "anthropic/claude-3-5-sonnet"
            assert model.name == "Claude 3.5 Sonnet"
    
    @pytest.mark.asyncio
    async def test_get_model_by_id_not_found(self, manager, sample_models):
        """Test getting a non-existent model by ID."""
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            model = await manager.get_model_by_id("nonexistent/model")
            
            assert model is None
    
    @pytest.mark.asyncio
    async def test_suggest_models_simple_task(self, manager, sample_models):
        """Test model suggestions for simple tasks."""
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            suggestions = await manager.suggest_models(
                "simple hello world program",
                max_suggestions=3
            )
            
            assert len(suggestions) > 0
            assert len(suggestions) <= 3
            
            # Should prefer cheaper models for simple tasks
            free_model_suggested = any(
                s.model.pricing.get("prompt", 0) == 0 for s in suggestions
            )
            assert free_model_suggested
    
    @pytest.mark.asyncio
    async def test_suggest_models_complex_task(self, manager, sample_models):
        """Test model suggestions for complex tasks."""
        models = [OpenRouterModel(**model) for model in sample_models]
        with patch.object(manager, 'list_models', return_value=models):
            
            suggestions = await manager.suggest_models(
                "complex function with tool integration",
                max_suggestions=3
            )
            
            assert len(suggestions) > 0
            
            # Should prefer models with tool support
            tool_model_suggested = any(
                s.model.supports_tools for s in suggestions
            )
            assert tool_model_suggested
    
    def test_estimate_cost(self, manager, sample_models):
        """Test cost estimation functionality."""
        model = OpenRouterModel(**sample_models[0])  # Claude model
        
        cost = manager._estimate_cost(model, "Generate a simple hello world program")
        
        assert cost > 0
        assert isinstance(cost, float)
    
    def test_cache_validation(self, manager):
        """Test cache validation logic."""
        # Test with non-existent cache file
        assert not manager._is_cache_valid()
        
        # Test with mock cache file
        with patch('pathlib.Path.exists', return_value=True):
            with patch('pathlib.Path.stat') as mock_stat:
                import time
                # Mock recent file
                mock_stat.return_value.st_mtime = time.time() - 1800  # 30 minutes ago
                assert manager._is_cache_valid()
                
                # Mock old file
                mock_stat.return_value.st_mtime = time.time() - 7200  # 2 hours ago
                assert not manager._is_cache_valid()
    
    def test_save_and_load_cache(self, manager, sample_models, tmp_path):
        """Test cache save and load functionality."""
        # Setup temporary cache file
        manager.cache_file = tmp_path / "test_cache.json"
        
        models = [OpenRouterModel(**model) for model in sample_models]
        
        # Test save
        manager._save_to_cache(models)
        assert manager.cache_file.exists()
        
        # Test load
        loaded_models = manager._load_from_cache()
        assert len(loaded_models) == len(models)
        assert loaded_models[0].id == models[0].id
    
    def test_clear_cache(self, manager, tmp_path):
        """Test cache clearing functionality."""
        # Create dummy cache file
        manager.cache_file = tmp_path / "test_cache.json"
        manager.cache_file.write_text("dummy content")
        
        assert manager.cache_file.exists()
        
        manager.clear_cache()
        
        assert not manager.cache_file.exists()
    
    def test_get_cache_info(self, manager, tmp_path):
        """Test cache information retrieval."""
        # Test with no cache
        info = manager.get_cache_info()
        assert info["exists"] == False
        
        # Test with cache
        manager.cache_file = tmp_path / "test_cache.json"
        manager.cache_file.write_text("test content")
        
        info = manager.get_cache_info()
        assert info["exists"] == True
        assert "size" in info
        assert "created" in info
    
    def test_update_metrics(self, manager):
        """Test performance metrics updating."""
        model_id = "test/model"
        
        # Update metrics
        manager.update_metrics(model_id, True, 1.5, 1000, 0.001)
        
        assert model_id in manager.metrics
        metrics = manager.metrics[model_id]
        assert metrics.total_requests == 1
        assert metrics.successful_requests == 1
        assert metrics.failed_requests == 0
        assert metrics.average_response_time == 1.5
        assert metrics.total_tokens_used == 1000
        assert metrics.total_cost == 0.001
    
    def test_get_metrics(self, manager):
        """Test metrics retrieval."""
        model_id = "test/model"
        manager.update_metrics(model_id, True, 1.0, 500, 0.0005)
        
        # Get all metrics
        all_metrics = manager.get_metrics()
        assert model_id in all_metrics
        
        # Get specific model metrics
        specific_metrics = manager.get_metrics(model_id)
        assert model_id in specific_metrics
        assert specific_metrics[model_id].total_requests == 1
    
    @pytest.mark.asyncio
    async def test_list_models_retry_logic(self, manager):
        """Test retry logic on API failures."""
        # Mock consecutive failures then success
        mock_responses = [
            httpx.HTTPError("Connection failed"),
            httpx.HTTPError("Connection failed"),
            Mock(status_code=200, json=lambda: {"data": []})
        ]
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = mock_responses
            
            # Should succeed after retries
            models = await manager.list_models(use_cache=False)
            assert models == []
    
    @pytest.mark.asyncio
    async def test_list_models_max_retries_exceeded(self, manager):
        """Test behavior when max retries are exceeded."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.HTTPError("Persistent failure")
            
            with pytest.raises(ModelManagerError) as exc_info:
                await manager.list_models(use_cache=False)
            
            assert "Failed to fetch models after" in str(exc_info.value)


@pytest.mark.asyncio
async def test_model_manager_initialization():
    """Test ModelManager initialization."""
    settings = Settings(
        openrouter=OpenRouterSettings(api_key="test_key"),
        flex=FlexSettings(),
        app=ApplicationSettings()
    )
    
    manager = ModelManager(settings)
    
    assert manager.api_key == "test_key"
    assert manager.base_url == "https://openrouter.ai/api/v1"
    assert manager.cache_file.name == "models_cache.json"