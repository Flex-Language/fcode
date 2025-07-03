#!/usr/bin/env python3
"""
Comprehensive test for the Flex AI Agent streaming functionality.
This test verifies that the streaming works without errors.
"""

import asyncio
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings

async def test_basic_streaming():
    """Test basic streaming functionality."""
    print("🧪 Testing basic streaming...")
    
    try:
        # Initialize agent
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        # Test simple request
        test_input = "Hello!"
        print(f"Input: {test_input}")
        print("Output: ", end="")
        
        response_parts = []
        async for chunk in agent.run_stream(test_input):
            if hasattr(chunk, 'kind'):
                if chunk.kind == 'response':
                    content = chunk.content
                    if response_parts and content.startswith(''.join(response_parts)):
                        # Full content, extract new part
                        new_content = content[len(''.join(response_parts)):]
                        if new_content:
                            print(new_content, end='')
                            response_parts = [content]  # Store full content
                    else:
                        # Delta content
                        print(content, end='')
                        response_parts.append(content)
            else:
                # Simple string
                content = str(chunk)
                print(content, end='')
                response_parts.append(content)
        
        print("\n✅ Basic streaming test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Basic streaming test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_flex_code_request():
    """Test Flex code generation request."""
    print("\n🧪 Testing Flex code generation...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        test_input = "Write a simple hello world program in Flex"
        print(f"Input: {test_input}")
        print("Output: ", end="")
        
        response_content = ""
        last_content = ""
        
        async for chunk in agent.run_stream(test_input):
            if hasattr(chunk, 'kind'):
                if chunk.kind == 'response':
                    content = chunk.content
                    if content.startswith(last_content):
                        new_content = content[len(last_content):]
                        if new_content:
                            print(new_content, end='')
                            last_content = content
                    else:
                        print(content, end='')
                        response_content += content
                elif chunk.kind == 'tool-call':
                    print(f"\n[Tool: {chunk.tool_name}]", end='')
            else:
                content = str(chunk)
                print(content, end='')
                response_content += content
        
        print("\n✅ Flex code generation test passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Flex code generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Run all tests."""
    print("🚀 Starting Flex AI Agent streaming tests...\n")
    
    tests = [
        test_basic_streaming,
        test_flex_code_request
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if await test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The streaming functionality is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
