#!/usr/bin/env python3
"""
Simple test to verify file creation tools work.
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings

async def test_simple_file_creation():
    """Test that the agent can create files when requested."""
    print("🧪 Testing Simple File Creation")
    print("=" * 50)
    
    # Initialize agent
    settings = get_settings()
    agent = FlexAIAgent(settings)
    
    print("Step 1: Test create_file tool directly")
    # This bypasses AI generation and tests the tool directly
    response1 = await agent.run("create_file filename=\"test_sample.lx\" content=\"etb3('Hello from Flex!')\"")
    print("Tool Response:")
    print(response1[:200] + "..." if len(response1) > 200 else response1)
    
    # Check if file was created
    if os.path.exists("test_sample.lx"):
        print("\n✅ SUCCESS: File 'test_sample.lx' was created!")
        with open("test_sample.lx", "r") as f:
            content = f.read()
        print(f"File contents: {content}")
        
        # Clean up
        os.remove("test_sample.lx")
        print("🧹 Test file cleaned up.")
    else:
        print("\n❌ ISSUE: File 'test_sample.lx' was not created.")
        print("The create_file tool may not be working properly.")
    
    print("\n" + "=" * 50)
    print("🎯 Simple File Creation Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_simple_file_creation())