#!/usr/bin/env python3
"""Test script for streaming functionality."""

import asyncio
from agents.flex_agent import FlexAIAgent
from config.settings import get_settings

async def test_streaming():
    """Test the streaming functionality."""
    print("Testing streaming functionality...")
    
    # Initialize agent
    settings = get_settings()
    agent = FlexAIAgent(settings)
    
    # Test simple request
    test_input = "Hello, can you help me with Flex programming?"
    
    print(f"Sending: {test_input}")
    print("Response: ", end="")
    
    try:
        async for chunk in agent.run_stream(test_input):
            if hasattr(chunk, 'kind'):
                if chunk.kind == 'response':
                    print(chunk.content, end='')
                elif chunk.kind == 'tool-call':
                    print(f"\n[Tool: {chunk.tool_name}]", end='')
            else:
                # Handle simple string response
                print(str(chunk), end='')
        
        print("\n\nTest completed successfully!")
        
    except Exception as e:
        print(f"\nError during streaming: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_streaming())
