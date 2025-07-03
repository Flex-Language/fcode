#!/usr/bin/env python3
"""
Test non-streaming functionality to debug the issue.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings

async def test_non_streaming():
    """Test non-streaming functionality."""
    print("🧪 Testing non-streaming functionality...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        test_input = "Hello!"
        print(f"Input: {test_input}")
        
        # Test non-streaming
        result = await agent.run(test_input)
        print(f"Output: {result}")
        
        print("\n✅ Non-streaming test completed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_non_streaming())
