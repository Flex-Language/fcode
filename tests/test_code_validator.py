"""
Unit tests for Flex Code Validator.

These tests validate the core Flex code validation functionality,
especially the critical Franco l7d loop safety checks.
"""

import pytest
import asyncio
from pathlib import Path
from unittest.mock import Mock, patch

from tools.code_validator import FlexCodeValidator
from agents.models import FlexSyntaxStyle, FlexError


class TestFlexCodeValidator:
    """Test suite for FlexCodeValidator."""
    
    @pytest.fixture
    def validator(self):
        """Create validator instance for testing."""
        # Mock the spec file to avoid dependency on external file
        mock_spec = {
            'ai_system_prompt': {
                'description': 'Test system prompt'
            }
        }
        
        with patch.object(FlexCodeValidator, '_load_spec', return_value=mock_spec):
            return FlexCodeValidator()
    
    def test_syntax_style_detection_franco(self, validator):
        """Test detection of Franco syntax style."""
        franco_code = """
        rakm counter = 0
        karr i=0 l7d 10 {
            etb3(i)
        }
        """
        
        style = validator._detect_syntax_style(franco_code)
        assert style == FlexSyntaxStyle.FRANCO
    
    def test_syntax_style_detection_english(self, validator):
        """Test detection of English syntax style."""
        english_code = """
        int counter = 0
        for(i=0; i<10; i++) {
            print(i)
        }
        """
        
        style = validator._detect_syntax_style(english_code)
        assert style == FlexSyntaxStyle.ENGLISH
    
    def test_syntax_style_detection_mixed(self, validator):
        """Test detection of mixed syntax style."""
        mixed_code = """
        rakm counter = 0
        for(i=0; i<10; i++) {
            etb3(i)
        }
        """
        
        style = validator._detect_syntax_style(mixed_code)
        assert style == FlexSyntaxStyle.MIXED
    
    @pytest.mark.asyncio
    async def test_franco_loop_safety_unsafe(self, validator):
        """Test detection of unsafe Franco l7d loops."""
        unsafe_code = """
        dorg myArray = [1, 2, 3, 4, 5]
        karr i=0 l7d length(myArray) {
            etb3(myArray[i])
        }
        """
        
        result = await validator.validate_code(unsafe_code)
        
        assert not result.is_valid
        assert result.has_franco_loop_safety_issues
        assert any(error.is_franco_loop_error for error in result.errors)
        assert any("out-of-bounds" in error.message for error in result.errors)
    
    @pytest.mark.asyncio
    async def test_franco_loop_safety_safe(self, validator):
        """Test validation of safe Franco l7d loops."""
        safe_code = """
        dorg myArray = [1, 2, 3, 4, 5]
        karr i=0 l7d length(myArray) - 1 {
            etb3(myArray[i])
        }
        """
        
        result = await validator.validate_code(safe_code)
        
        # Should not have Franco loop safety issues
        assert not result.has_franco_loop_safety_issues
        franco_errors = [error for error in result.errors if error.is_franco_loop_error]
        assert len(franco_errors) == 0
    
    @pytest.mark.asyncio
    async def test_semicolon_detection(self, validator):
        """Test detection of semicolons (not allowed in Flex)."""
        code_with_semicolons = """
        rakm x = 10;
        etb3(x);
        """
        
        result = await validator.validate_code(code_with_semicolons)
        
        assert not result.is_valid
        semicolon_errors = [error for error in result.errors if "semicolon" in error.message.lower()]
        assert len(semicolon_errors) == 2  # Two semicolons
    
    @pytest.mark.asyncio
    async def test_unmatched_braces(self, validator):
        """Test detection of unmatched braces."""
        code_with_unmatched_braces = """
        lw condition {
            etb3("hello")
        """
        
        result = await validator.validate_code(code_with_unmatched_braces)
        
        assert not result.is_valid
        brace_errors = [error for error in result.errors if "brace" in error.message.lower()]
        assert len(brace_errors) > 0
    
    @pytest.mark.asyncio
    async def test_division_by_zero_detection(self, validator):
        """Test detection of division by zero."""
        code_with_division_by_zero = """
        rakm result = 10 / 0
        """
        
        result = await validator.validate_code(code_with_division_by_zero)
        
        assert not result.is_valid
        division_errors = [error for error in result.errors if "division by zero" in error.message.lower()]
        assert len(division_errors) == 1
    
    def test_franco_loop_safety_specific_validation(self, validator):
        """Test specific Franco loop safety validation function."""
        unsafe_code = """
        karr i=0 l7d length(myArray) {
            print(myArray[i])
        }
        """
        
        is_safe, errors = validator.validate_franco_loop_safety(unsafe_code)
        
        assert not is_safe
        assert len(errors) == 1
        assert errors[0].is_franco_loop_error
    
    def test_franco_loop_safety_fix(self, validator):
        """Test automatic fixing of Franco loop safety issues."""
        unsafe_code = """
        karr i=0 l7d length(myArray) {
            print(myArray[i])
        }
        """
        
        fixed_code = validator.fix_franco_loop_safety(unsafe_code)
        
        assert "length(myArray) - 1" in fixed_code
        assert "length(myArray) {" not in fixed_code
    
    def test_safe_franco_loop_examples(self, validator):
        """Test that safe Franco loop examples are provided."""
        examples = validator.get_safe_franco_loop_examples()
        
        assert "safe_array_iteration" in examples
        assert "unsafe_pattern" in examples
        assert "alternative_english" in examples
        
        # Check that safe example contains proper bounds
        safe_example = examples["safe_array_iteration"]
        assert "length(myArray) - 1" in safe_example
    
    @pytest.mark.asyncio
    async def test_valid_code_validation(self, validator):
        """Test validation of completely valid code."""
        valid_code = """
        rakm x = 10
        rakm y = 20
        rakm sum = x + y
        etb3("Sum is: " + sum)
        """
        
        result = await validator.validate_code(valid_code)
        
        assert result.is_valid
        assert len(result.errors) == 0
        assert not result.has_franco_loop_safety_issues
    
    @pytest.mark.asyncio
    async def test_warning_generation(self, validator):
        """Test generation of warnings for potential issues."""
        code_with_warnings = """
        rakm a = 10  // Single letter variable
        karr i=0 l7d 5 { etb3(i) }  // This line is intentionally very long to trigger a warning about line length exceeding the recommended limit
        """
        
        result = await validator.validate_code(code_with_warnings)
        
        # Should have warnings but still be valid
        assert len(result.warnings) > 0
    
    @pytest.mark.asyncio
    async def test_suggestion_generation(self, validator):
        """Test generation of improvement suggestions."""
        code_needing_suggestions = """
        rakm x = da5l()
        rakm result = x / 5
        """
        
        result = await validator.validate_code(code_needing_suggestions)
        
        # Should generate suggestions for input validation and error handling
        assert len(result.suggestions) > 0
        assert any("input validation" in suggestion.lower() for suggestion in result.suggestions)
    
    def test_contains_array_access_after_loop(self, validator):
        """Test detection of array access after loop patterns."""
        lines = [
            "karr i=0 l7d 10 {",
            "    etb3(arr[i])",
            "}"
        ]
        
        # Should detect array access in line after loop
        has_access = validator._contains_array_access_after_loop(lines, 0)
        assert has_access
    
    def test_matches_filter_criteria(self, validator):
        """Test internal filter matching logic."""
        from agents.models import OpenRouterModel, ModelFilter
        
        # Create mock model
        model = OpenRouterModel(
            id="test/model",
            name="Test Model",
            pricing={"prompt": 0.00001, "completion": 0.00005},
            context_length=100000,
            top_provider="Test Provider"
        )
        
        # Test price filter
        price_filter = ModelFilter(max_price_prompt=0.00002)
        assert validator._matches_filter(model, price_filter)
        
        # Test context length filter
        context_filter = ModelFilter(min_context_length=50000)
        assert validator._matches_filter(model, context_filter)
        
        # Test search term filter
        search_filter = ModelFilter(search_term="test")
        assert validator._matches_filter(model, search_filter)


@pytest.mark.asyncio
async def test_validator_initialization():
    """Test validator initialization with missing spec file."""
    with patch('pathlib.Path.open', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            FlexCodeValidator()


@pytest.mark.asyncio
async def test_validator_initialization_invalid_json():
    """Test validator initialization with invalid JSON spec file."""
    with patch('pathlib.Path.open', side_effect=Exception("Invalid JSON")):
        with pytest.raises(Exception):
            FlexCodeValidator()


def test_compile_patterns():
    """Test that regex patterns compile correctly."""
    # This will fail if any patterns have syntax errors
    mock_spec = {'ai_system_prompt': {'description': 'Test'}}
    
    with patch.object(FlexCodeValidator, '_load_spec', return_value=mock_spec):
        validator = FlexCodeValidator()
        
        # Check that patterns are compiled
        assert validator.franco_patterns['loop'] is not None
        assert validator.english_patterns['loop'] is not None
        assert validator.safety_patterns['franco_unsafe_loop'] is not None