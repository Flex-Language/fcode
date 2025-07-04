#!/usr/bin/env python3
"""
Test script to verify the agent improvements are working correctly.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings


async def test_agent_initialization():
    """Test that the agent initializes correctly with file reference."""
    print("🧪 Testing agent initialization...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        # Check that flex_spec was loaded
        if agent.flex_spec:
            print("✅ Flex language spec loaded successfully")
            if 'ai_system_prompt' in agent.flex_spec:
                print("✅ AI system prompt found in spec")
            else:
                print("⚠️  Using fallback system prompt with #file reference")
        else:
            print("❌ Failed to load flex spec")
            return False
            
        # Check that agent was created
        if agent.agent:
            print("✅ PydanticAI agent created successfully")
        else:
            print("❌ Failed to create PydanticAI agent")
            return False
            
        print(f"✅ Current model: {agent.current_model_id}")
        return True
        
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}")
        return False


async def test_simple_request():
    """Test a simple request to verify the agent works."""
    print("\n🧪 Testing simple AI request...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        # Simple test request
        response = await agent.run("What is Flex programming language?")
        
        if response and len(response.strip()) > 10:
            print("✅ Agent responded successfully")
            print(f"Response preview: {response[:100]}...")
            return True
        else:
            print("❌ Agent response was empty or too short")
            return False
            
    except Exception as e:
        print(f"❌ Simple request failed: {e}")
        return False


async def main():
    """Run all tests."""
    print("🚀 Testing Flex AI Agent improvements...\n")
    
    # Test 1: Agent initialization
    init_success = await test_agent_initialization()
    
    if not init_success:
        print("\n❌ Basic initialization failed. Cannot proceed with further tests.")
        return
    
    # Test 2: Simple request (optional - may fail if no API key)
    try:
        request_success = await test_simple_request()
        if request_success:
            print("✅ All tests passed!")
        else:
            print("⚠️  Basic tests passed, but AI request failed (may be API key issue)")
    except Exception as e:
        print(f"⚠️  AI request test skipped due to: {e}")
        print("✅ Basic agent initialization tests passed!")


if __name__ == "__main__":
    asyncio.run(main())
