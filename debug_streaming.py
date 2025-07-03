#!/usr/bin/env python3
"""
Debug the exact structure of PydanticAI streaming chunks.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings

async def debug_streaming_structure():
    """Debug the exact structure of streaming chunks."""
    print("🔍 Debugging streaming structure...")
    
    try:
        settings = get_settings()
        agent = FlexAIAgent(settings)
        
        test_input = "Hello!"
        print(f"Input: {test_input}")
        print("Analyzing chunks:")
        
        chunk_count = 0
        async for chunk in agent.run_stream(test_input):
            chunk_count += 1
            print(f"\nChunk {chunk_count}:")
            print(f"  Type: {type(chunk)}")
            print(f"  Str representation: {repr(str(chunk))}")
            
            if hasattr(chunk, '__dict__'):
                print(f"  Attributes: {chunk.__dict__}")
            
            if hasattr(chunk, 'kind'):
                print(f"  Kind: {chunk.kind}")
                if hasattr(chunk, 'content'):
                    print(f"  Content: {repr(chunk.content)}")
            
            # Limit to first 5 chunks to avoid spam
            if chunk_count >= 5:
                print("  ... (truncated)")
                break
        
        print(f"\nTotal chunks processed: {chunk_count}")
        
    except Exception as e:
        print(f"\n❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_streaming_structure())
