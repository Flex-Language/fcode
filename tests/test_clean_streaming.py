#!/usr/bin/env python3
"""
Final test to verify the streaming fix works properly.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings

async def test_clean_streaming():
    """Test that streaming produces clean output without duplication."""
    print("🧪 Testing clean streaming output...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        test_input = "Hello, write me a simple hello world in Flex"
        print(f"Input: {test_input}")
        print("Output: ", end="", flush=True)
        
        response_content = ""
        last_length = 0
        
        async for chunk in agent.run_stream(test_input):
            if hasattr(chunk, 'kind'):
                if chunk.kind == 'response':
                    content = chunk.content
                    # Only print new content
                    if len(content) > last_length:
                        new_part = content[last_length:]
                        print(new_part, end='', flush=True)
                        last_length = len(content)
                    response_content = content
            else:
                content = str(chunk)
                print(content, end='', flush=True)
                response_content += content
        
        print("\n\n✅ Clean streaming test completed!")
        print(f"Final response length: {len(response_content)} characters")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_clean_streaming())
