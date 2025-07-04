#!/usr/bin/env python3
"""
Debug the streaming issue in the Flex AI Agent.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings


async def debug_streaming():
    """Debug the streaming functionality."""
    print("🐛 DEBUGGING STREAMING ISSUE")
    print("=" * 40)
    
    try:
        # Initialize agent
        settings = get_settings()
        agent = FlexAIAgent(settings)
        print("✅ Agent initialized")
        
        # Test simple input
        test_input = "Hello, create a simple hello world in Franco syntax"
        print(f"📝 Testing input: {test_input}")
        
        # Test non-streaming first
        print("\n🔄 Testing non-streaming approach:")
        try:
            response = await asyncio.wait_for(
                agent.run(test_input), 
                timeout=30
            )
            print(f"✅ Non-streaming response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Non-streaming failed: {e}")
        
        # Test streaming
        print("\n📡 Testing streaming approach:")
        try:
            chunk_count = 0
            response_content = ""
            
            async for chunk in agent.run_stream(test_input):
                chunk_count += 1
                chunk_str = str(chunk)
                response_content = chunk_str  # PydanticAI gives cumulative content
                print(f"📦 Chunk {chunk_count}: {len(chunk_str)} chars")
                
                if chunk_count >= 5:  # Limit output for debugging
                    print("   ... (truncated for debugging)")
                    break
            
            print(f"✅ Streaming completed: {chunk_count} chunks, {len(response_content)} total chars")
            
        except Exception as e:
            print(f"❌ Streaming failed: {e}")
            import traceback
            traceback.print_exc()
        
        return True
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_api_connection():
    """Test basic API connectivity."""
    print(f"\n🌐 TESTING API CONNECTION")
    print("=" * 40)
    
    try:
        import httpx
        
        # Test OpenRouter API directly
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            print("❌ No API key found")
            return False
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Simple test request
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://openrouter.ai/api/v1/models",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ API connection successful")
                models = response.json()
                print(f"📊 Found {len(models.get('data', []))} models")
                return True
            else:
                print(f"❌ API connection failed: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


async def main():
    """Run debugging tests."""
    print("🐛 FLEX AGENT STREAMING DEBUG")
    print("=" * 50)
    
    # Test API connection first
    api_ok = await test_api_connection()
    
    if api_ok:
        # Test agent streaming
        agent_ok = await debug_streaming()
        
        if agent_ok:
            print(f"\n🎯 DIAGNOSIS:")
            print("The agent streaming should be working.")
            print("If CLI still hangs, the issue might be in the CLI streaming logic.")
        else:
            print(f"\n🎯 DIAGNOSIS:")
            print("The agent streaming has issues.")
            print("This explains why the CLI hangs during AI requests.")
    else:
        print(f"\n🎯 DIAGNOSIS:")
        print("API connection issues detected.")
        print("This explains why the CLI hangs - network/auth problems.")
    
    print(f"\n💡 RECOMMENDATIONS:")
    print("1. Check your internet connection")
    print("2. Verify OPENROUTER_API_KEY is valid")
    print("3. Try a different model (some might be down)")
    print("4. Use offline features: validate, models, help")


if __name__ == "__main__":
    asyncio.run(main())