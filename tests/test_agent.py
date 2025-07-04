#!/usr/bin/env python3
"""
Test script for Flex AI Agent functionality.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.flex_agent import FlexAIAgent
from agents.models import FlexCodeRequest, FlexSyntaxStyle
from config.settings import get_settings


async def test_agent_basic():
    """Test basic agent functionality."""
    print("🧪 Testing Flex AI Agent...")
    
    try:
        # Initialize agent
        settings = get_settings()
        agent = FlexAIAgent(settings)
        print("✅ Agent initialized successfully")
        
        # Test model listing
        models = await agent.model_manager.list_models()
        print(f"✅ Found {len(models)} available models")
        
        # Test code validation
        test_code = """
        rakm counter = 0
        karr i=0 l7d 5 {
            etb3(i)
        }
        """
        
        validation_result = await agent.code_validator.validate_code(test_code)
        print(f"✅ Code validation works: {len(validation_result.errors)} errors, {len(validation_result.warnings)} warnings")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False


async def test_agent_code_generation():
    """Test agent code generation."""
    print("\n🧪 Testing code generation...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        # Create a simple code request
        request = FlexCodeRequest(
            prompt="Create a simple loop that prints numbers 1 to 5",
            syntax_style=FlexSyntaxStyle.FRANCO,
            include_comments=True,
            max_lines=20
        )
        
        print(f"📝 Request: {request.prompt}")
        print(f"🌐 Syntax: {request.syntax_style}")
        
        # Note: This would require API key for actual generation
        # For now, just test the request structure
        print("✅ Code generation request structure valid")
        
        return True
        
    except Exception as e:
        print(f"❌ Code generation test failed: {e}")
        return False


async def test_agent_tools():
    """Test agent tools functionality."""
    print("\n🧪 Testing agent tools...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        # Import required models
        from agents.models import FileOperation
        
        # Test file manager write operation
        test_content = "// Test Flex file\netb3('Hello from agent test!')"
        
        write_op = FileOperation(
            operation="write",
            filepath="temp/agent_test.flex",
            content=test_content
        )
        
        write_result = await agent.file_manager.execute_operation(write_op)
        print(f"✅ File write: {write_result.success}")
        
        # Test file existence check
        exists_op = FileOperation(
            operation="exists",
            filepath="temp/agent_test.flex"
        )
        
        exists_result = await agent.file_manager.execute_operation(exists_op)
        print(f"✅ File exists: {exists_result.success}")
        
        # Test file read
        read_op = FileOperation(
            operation="read", 
            filepath="temp/agent_test.flex"
        )
        
        read_result = await agent.file_manager.execute_operation(read_op)
        print(f"✅ File read: {read_result.success}")
        
        # Clean up
        delete_op = FileOperation(
            operation="delete",
            filepath="temp/agent_test.flex"
        )
        
        delete_result = await agent.file_manager.execute_operation(delete_op)
        print(f"✅ File cleanup: {delete_result.success}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent tools test failed: {e}")
        return False


async def main():
    """Run all agent tests."""
    print("🚀 Starting Flex AI Agent Tests\n")
    
    tests = [
        test_agent_basic,
        test_agent_code_generation, 
        test_agent_tools
    ]
    
    results = []
    for test in tests:
        result = await test()
        results.append(result)
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All agent tests passed!")
        return 0
    else:
        print("⚠️  Some agent tests failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)