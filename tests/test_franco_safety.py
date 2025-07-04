#!/usr/bin/env python3
"""
Critical test for Franco l7d loop safety - the #1 source of runtime errors.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings


async def test_franco_loop_safety():
    """Test the critical Franco loop safety validation."""
    print("🚨 FRANCO L7D LOOP SAFETY TEST")
    print("=" * 40)
    print("Testing the #1 source of Flex runtime errors...\n")
    
    agent = FlexAIAgent(get_settings())
    
    # Test cases for Franco loop safety
    test_cases = [
        {
            "name": "🔥 UNSAFE: Direct length() in l7d",
            "code": """
            dorg myArray = [1, 2, 3, 4, 5]
            karr i=0 l7d length(myArray) {
                etb3(myArray[i])
            }
            """,
            "should_be_unsafe": True
        },
        {
            "name": "✅ SAFE: length() - 1 in l7d", 
            "code": """
            dorg myArray = [1, 2, 3, 4, 5]
            karr i=0 l7d length(myArray) - 1 {
                etb3(myArray[i])
            }
            """,
            "should_be_unsafe": False
        },
        {
            "name": "🔥 UNSAFE: Hardcoded array length",
            "code": """
            dorg numbers = [10, 20, 30]
            karr i=0 l7d 3 {
                etb3(numbers[i])
            }
            """,
            "should_be_unsafe": True
        },
        {
            "name": "✅ SAFE: Hardcoded length - 1",
            "code": """
            dorg numbers = [10, 20, 30] 
            karr i=0 l7d 2 {
                etb3(numbers[i])
            }
            """,
            "should_be_unsafe": False
        },
        {
            "name": "✅ SAFE: Non-array loop",
            "code": """
            karr i=0 l7d 5 {
                etb3("Number: " + i)
            }
            """,
            "should_be_unsafe": False
        }
    ]
    
    results = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"📝 Test {i}: {test_case['name']}")
        
        try:
            validation = await agent.code_validator.validate_code(test_case['code'])
            
            has_safety_issues = validation.has_franco_loop_safety_issues
            has_errors = len(validation.errors) > 0
            
            # Check if our detection matches expected result
            detected_unsafe = has_safety_issues or has_errors
            expected_unsafe = test_case['should_be_unsafe']
            
            if detected_unsafe == expected_unsafe:
                status = "✅ CORRECT"
                results.append(True)
            else:
                status = "❌ WRONG"
                results.append(False)
            
            print(f"   {status} - Safety issues: {has_safety_issues}, Errors: {has_errors}")
            
            if has_errors:
                print(f"   🚨 Error: {validation.errors[0].message}")
            
            if validation.suggestions:
                print(f"   💡 Suggestion: {validation.suggestions[0]}")
                
        except Exception as e:
            print(f"   ❌ FAILED: {e}")
            results.append(False)
        
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("📊 FRANCO SAFETY TEST RESULTS")
    print("=" * 40)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {passed/total*100:.1f}%")
    
    if passed == total:
        print("🎉 ALL FRANCO SAFETY TESTS PASSED!")
        print("🛡️  The agent correctly identifies unsafe Franco l7d loops!")
        print("🚀 Critical Flex safety feature is working perfectly!")
    else:
        print("⚠️  Some Franco safety tests failed")
        print("🔧 Franco loop safety detection needs improvement")
    
    return passed == total


async def main():
    """Run Franco safety tests."""
    success = await test_franco_loop_safety()
    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)