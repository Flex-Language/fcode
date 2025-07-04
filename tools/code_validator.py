"""
Flex Code Validator for the Flex AI Agent.

This module validates Flex code against the language specification with special
emphasis on Franco l7d loop safety (the #1 source of runtime errors).
"""

import re
import json
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

from agents.models import (
    FlexSyntaxStyle,
    FlexError,
    CodeValidationResult
)


class FlexCodeValidator:
    """Validates Flex code for syntax correctness and safety issues."""
    
    def __init__(self, spec_path: str = "data/flex_language_spec.json"):
        """Initialize validator with language specification."""
        self.spec_path = Path(spec_path)
        self.spec = self._load_spec()
        
        # Compile regex patterns for efficient validation
        self._compile_patterns()
    
    def _load_spec(self) -> Dict[str, Any]:
        """Load Flex language specification."""
        try:
            with open(self.spec_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Flex language spec not found at {self.spec_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in language spec: {e}")
    
    def _compile_patterns(self) -> None:
        """Compile regex patterns for syntax validation."""
        # Franco syntax patterns
        self.franco_patterns = {
            'loop': re.compile(r'\bkarr\s+(\w+\s*=\s*\d+\s+)?l7d\s+([^{]+)\s*\{'),
            'variable': re.compile(r'\b(rakm|kasr|so2al|klma|dorg)\s+\w+'),
            'function': re.compile(r'\bsndo2\s+\w+\s*\([^)]*\)\s*\{'),
            'conditional': re.compile(r'\blw\s+[^{]+\s*\{'),
            'print': re.compile(r'\betb3\s*\([^)]+\)'),
            'input': re.compile(r'\bda5l\s*\(\s*\)'),
            'boolean_true': re.compile(r'\bsa7\b'),
            'boolean_false': re.compile(r'\bghalt\b'),
            'while_loop': re.compile(r'\btalama\s+[^{]+\s*\{'),
            'else': re.compile(r'\bgher\s*\{'),
            'return': re.compile(r'\brg3\s')
        }
        
        # English syntax patterns
        self.english_patterns = {
            'loop': re.compile(r'\bfor\s*\([^)]+\)\s*\{'),
            'variable': re.compile(r'\b(int|float|bool|string|list)\s+\w+'),
            'function': re.compile(r'\bfun\s+\w+\s*\([^)]*\)\s*\{'),
            'conditional': re.compile(r'\bif\s*\([^)]+\)\s*\{'),
            'print': re.compile(r'\bprint\s*\([^)]+\)'),
            'input': re.compile(r'\bscan\s*\(\s*\)'),
            'boolean_true': re.compile(r'\btrue\b'),
            'boolean_false': re.compile(r'\bfalse\b'),
            'while_loop': re.compile(r'\bwhile\s*\([^)]+\)\s*\{'),
            'else': re.compile(r'\belse\s*\{'),
            'return': re.compile(r'\breturn\s')
        }
        
        # Critical safety patterns
        self.safety_patterns = {
            'franco_unsafe_loop': re.compile(r'\bkarr\s+\w+\s*=\s*\d+\s+l7d\s+(length\s*\([^)]+\))\s*\{'),
            'array_access': re.compile(r'\w+\s*\[\s*([^]]+)\s*\]'),
            'division_by_zero': re.compile(r'/\s*0\b'),
            'modulo_by_zero': re.compile(r'%\s*0\b')
        }
        
        # Common error patterns
        self.error_patterns = {
            'semicolon': re.compile(r';'),  # Flex doesn't use semicolons
            'missing_brace_open': re.compile(r'\b(lw|if|karr|for|sndo2|fun|talama|while)\s+[^{]*$'),
            'missing_brace_close': re.compile(r'\{[^}]*$'),
            'undefined_variable': re.compile(r'\b[a-zA-Z_]\w*\b'),  # Will need context checking
        }
    
    async def validate_code(self, code: str) -> CodeValidationResult:
        """
        Validate Flex code for syntax and safety issues.
        
        Args:
            code: Flex code to validate
            
        Returns:
            Validation result with errors, warnings, and suggestions
        """
        errors = []
        warnings = []
        suggestions = []
        
        # Detect syntax style
        syntax_style = self._detect_syntax_style(code)
        
        # Core validation checks
        errors.extend(self._check_syntax_errors(code, syntax_style))
        errors.extend(self._check_safety_issues(code))
        
        # Warning checks
        warnings.extend(self._check_warnings(code, syntax_style))
        
        # Suggestion checks
        suggestions.extend(self._get_suggestions(code, syntax_style))
        
        # Check for Franco loop safety issues specifically
        has_franco_loop_safety_issues = any(
            error.is_franco_loop_error for error in errors
        )
        
        return CodeValidationResult(
            is_valid=len(errors) == 0,
            syntax_style=syntax_style,
            errors=errors,
            warnings=warnings,
            suggestions=suggestions,
            has_franco_loop_safety_issues=has_franco_loop_safety_issues
        )
    
    def _detect_syntax_style(self, code: str) -> FlexSyntaxStyle:
        """Detect the syntax style used in the code."""
        franco_count = 0
        english_count = 0
        
        # Count Franco patterns
        for pattern in self.franco_patterns.values():
            franco_count += len(pattern.findall(code))
        
        # Count English patterns
        for pattern in self.english_patterns.values():
            english_count += len(pattern.findall(code))
        
        # If both styles are present, it's mixed
        if franco_count > 0 and english_count > 0:
            return FlexSyntaxStyle.MIXED
        elif franco_count > english_count:
            return FlexSyntaxStyle.FRANCO
        elif english_count > franco_count:
            return FlexSyntaxStyle.ENGLISH
        else:
            return FlexSyntaxStyle.AUTO
    
    def _check_syntax_errors(self, code: str, syntax_style: FlexSyntaxStyle) -> List[FlexError]:
        """Check for basic syntax errors."""
        errors = []
        lines = code.split('\n')
        
        # Check for semicolons (not allowed in Flex)
        for line_num, line in enumerate(lines, 1):
            if self.error_patterns['semicolon'].search(line):
                errors.append(FlexError(
                    error_type="SyntaxError",
                    message="Semicolons are not allowed in Flex",
                    line_number=line_num,
                    suggestion="Remove the semicolon - Flex uses curly braces for code blocks",
                    prevention="Remember that Flex doesn't require semicolons at the end of statements"
                ))
        
        # Check for unmatched braces
        brace_count = 0
        for line_num, line in enumerate(lines, 1):
            brace_count += line.count('{') - line.count('}')
            if brace_count < 0:
                errors.append(FlexError(
                    error_type="SyntaxError",
                    message="Unmatched closing brace",
                    line_number=line_num,
                    suggestion="Add an opening brace '{' before this line",
                    prevention="Always match opening and closing braces"
                ))
                brace_count = 0  # Reset to continue checking
        
        if brace_count > 0:
            errors.append(FlexError(
                error_type="SyntaxError",
                message="Unmatched opening brace",
                line_number=len(lines),
                suggestion="Add closing braces '}' to match all opening braces",
                prevention="Always match opening and closing braces"
            ))
        
        return errors
    
    def _check_safety_issues(self, code: str) -> List[FlexError]:
        """Check for critical safety issues, especially Franco l7d loops."""
        errors = []
        lines = code.split('\n')
        
        # CRITICAL: Check for Franco l7d loop safety issues
        for line_num, line in enumerate(lines, 1):
            # Check for unsafe Franco loop patterns
            franco_loop_match = self.franco_patterns['loop'].search(line)
            if franco_loop_match:
                loop_condition = franco_loop_match.group(2).strip()
                
                # Check if loop uses length() without -1
                if 'length(' in loop_condition and ('- 1' not in loop_condition and '-1' not in loop_condition):
                    # Reason: This is the #1 source of runtime errors in Flex
                    errors.append(FlexError(
                        error_type="FrancoLoopSafetyError",
                        message="Franco l7d loops are INCLUSIVE - this will cause out-of-bounds array access",
                        line_number=line_num,
                        suggestion=f"Change '{loop_condition}' to '{loop_condition} - 1' for safe array access",
                        prevention="Always use 'length(array) - 1' in Franco l7d loops to avoid out-of-bounds errors",
                        is_franco_loop_error=True
                    ))
                
                # Check for other potentially unsafe patterns
                elif re.search(r'\b\d+\b', loop_condition) and 'length(' not in loop_condition:
                    # Warn about hardcoded values that might be array indices
                    if self._contains_array_access_after_loop(lines, line_num):
                        errors.append(FlexError(
                            error_type="PotentialArrayAccessError",
                            message="Franco loop with hardcoded limit may cause array access issues",
                            line_number=line_num,
                            suggestion="Verify that the loop limit doesn't exceed array bounds",
                            prevention="Use 'length(array) - 1' for array iteration or verify bounds manually",
                            is_franco_loop_error=True
                        ))
            
            # Check for division/modulo by zero
            if self.safety_patterns['division_by_zero'].search(line):
                errors.append(FlexError(
                    error_type="DivisionByZeroError",
                    message="Division by zero detected",
                    line_number=line_num,
                    suggestion="Add a check: lw divisor != 0 { ... } before division",
                    prevention="Always validate divisor is not zero before division operations"
                ))
            
            if self.safety_patterns['modulo_by_zero'].search(line):
                errors.append(FlexError(
                    error_type="ModuloByZeroError",
                    message="Modulo by zero detected",
                    line_number=line_num,
                    suggestion="Add a check: lw divisor != 0 { ... } before modulo operation",
                    prevention="Always validate divisor is not zero before modulo operations"
                ))
        
        return errors
    
    def _contains_array_access_after_loop(self, lines: List[str], loop_line: int) -> bool:
        """Check if there's array access in the lines following a loop."""
        # Check next 10 lines for array access patterns
        for i in range(loop_line, min(loop_line + 10, len(lines))):
            if self.safety_patterns['array_access'].search(lines[i]):
                return True
        return False
    
    def _check_warnings(self, code: str, syntax_style: FlexSyntaxStyle) -> List[str]:
        """Check for potential issues that aren't errors but should be warnings."""
        warnings = []
        lines = code.split('\n')
        
        # Check for mixed syntax styles
        if syntax_style == FlexSyntaxStyle.MIXED:
            warnings.append("Code mixes Franco and English syntax - consider using consistent style")
        
        # Check for potentially confusing variable names
        for line_num, line in enumerate(lines, 1):
            # Check for single-letter variables (except common ones like i, j, x, y)
            single_letter_vars = re.findall(r'\b[a-hk-wz]\b', line)
            if single_letter_vars:
                warnings.append(f"Line {line_num}: Consider using more descriptive variable names")
        
        # Check for long lines
        for line_num, line in enumerate(lines, 1):
            if len(line) > 120:
                warnings.append(f"Line {line_num}: Line is very long - consider breaking it up")
        
        return warnings
    
    def _get_suggestions(self, code: str, syntax_style: FlexSyntaxStyle) -> List[str]:
        """Get improvement suggestions for the code."""
        suggestions = []
        
        # Suggest consistent style
        if syntax_style == FlexSyntaxStyle.AUTO:
            suggestions.append("Consider using explicit Franco or English syntax for clarity")
        
        # Check for input validation
        if re.search(r'\b(da5l|scan)\s*\(\s*\)', code):
            suggestions.append("Consider adding input validation for user inputs")
        
        # Check for error handling
        if '/' in code and 'lw' not in code and 'if' not in code:
            suggestions.append("Consider adding error handling for division operations")
        
        # Check for comments
        if '#' not in code and '//' not in code:
            suggestions.append("Consider adding comments to explain complex logic")
        
        return suggestions
    
    def validate_franco_loop_safety(self, code: str) -> Tuple[bool, List[FlexError]]:
        """
        Specifically validate Franco l7d loop safety.
        
        Args:
            code: Code to validate
            
        Returns:
            Tuple of (is_safe, errors)
        """
        errors = []
        lines = code.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            franco_loop_match = self.franco_patterns['loop'].search(line)
            if franco_loop_match:
                loop_condition = franco_loop_match.group(2).strip()
                
                # Critical check for length() usage
                if 'length(' in loop_condition:
                    if '- 1' not in loop_condition and '-1' not in loop_condition:
                        errors.append(FlexError(
                            error_type="CriticalFrancoLoopError",
                            message="CRITICAL: Franco l7d loop will cause out-of-bounds access",
                            line_number=line_num,
                            suggestion=f"MUST CHANGE: '{loop_condition}' → '{loop_condition} - 1'",
                            prevention="Franco loops are INCLUSIVE - always use 'length(array) - 1'",
                            is_franco_loop_error=True
                        ))
        
        return len(errors) == 0, errors
    
    def get_safe_franco_loop_examples(self) -> Dict[str, str]:
        """Get examples of safe Franco loop patterns."""
        return {
            "safe_array_iteration": """
// SAFE: Franco l7d loop with proper bounds
dorg myArray = [1, 2, 3, 4, 5]
karr i=0 l7d length(myArray) - 1 {
    etb3(myArray[i])  // Safe access
}
""",
            "unsafe_pattern": """
// UNSAFE: Will cause out-of-bounds error!
dorg myArray = [1, 2, 3, 4, 5]
karr i=0 l7d length(myArray) {
    etb3(myArray[i])  // ERROR on last iteration!
}
""",
            "alternative_english": """
// SAFE: English style alternative
list myArray = [1, 2, 3, 4, 5]
for(i=0; i<length(myArray); i++) {
    print(myArray[i])  // Safe access
}
"""
        }
    
    def fix_franco_loop_safety(self, code: str) -> str:
        """
        Automatically fix Franco loop safety issues.
        
        Args:
            code: Code with potential Franco loop issues
            
        Returns:
            Fixed code with safe loop bounds
        """
        lines = code.split('\n')
        
        for i, line in enumerate(lines):
            franco_loop_match = self.franco_patterns['loop'].search(line)
            if franco_loop_match:
                loop_condition = franco_loop_match.group(2).strip()
                
                # Fix length() usage without -1
                if 'length(' in loop_condition and '- 1' not in loop_condition and '-1' not in loop_condition:
                    # Add - 1 to the length expression
                    fixed_condition = re.sub(
                        r'length\s*\([^)]+\)',
                        lambda m: f"{m.group(0)} - 1",
                        loop_condition
                    )
                    lines[i] = line.replace(loop_condition, fixed_condition)
        
        return '\n'.join(lines)