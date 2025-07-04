#!/usr/bin/env python3
"""
Fix the CLI hanging issue when no API key is provided.
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.settings import get_settings


def diagnose_api_key_issue():
    """Diagnose API key configuration issues."""
    print("🔍 DIAGNOSING CLI HANGING ISSUE")
    print("=" * 40)
    
    # Check environment variables
    openrouter_key = os.getenv('OPENROUTER_API_KEY')
    print(f"🔑 OPENROUTER_API_KEY environment variable: {'✅ Set' if openrouter_key else '❌ Not set'}")
    
    if openrouter_key:
        print(f"   Key preview: {openrouter_key[:8]}...{openrouter_key[-4:] if len(openrouter_key) > 12 else '[too short]'}")
    
    # Check settings
    try:
        settings = get_settings()
        settings_key = settings.openrouter.api_key
        print(f"🔧 Settings API key: {'✅ Set' if settings_key else '❌ Not set'}")
        
        if settings_key and settings_key != openrouter_key:
            print("⚠️  Environment and settings API keys differ!")
        
        print(f"🌐 OpenRouter base URL: {settings.openrouter.base_url}")
        print(f"🤖 Default model: {settings.app.default_model}")
        
    except Exception as e:
        print(f"❌ Settings error: {e}")
    
    # Provide solution
    print(f"\n💡 SOLUTION TO FIX HANGING:")
    if not openrouter_key:
        print("1. Set your OpenRouter API key:")
        print("   export OPENROUTER_API_KEY='your-api-key-here'")
        print("\n2. Get a free API key from: https://openrouter.ai/")
        print("\n3. Alternative: Use offline mode with validation only")
    
    print(f"\n🛠️  RECOMMENDED TESTING APPROACH:")
    print("   python main.py --validate flex_examples/franco_examples/hello_world.flex")
    print("   python main.py --models | head -10")
    

def test_timeout_handling():
    """Test if we can handle timeouts gracefully."""
    print(f"\n⏰ TESTING TIMEOUT HANDLING")
    print("=" * 40)
    
    async def timeout_test():
        try:
            # Simulate what happens when API call hangs
            await asyncio.sleep(2)  # Simulate delay
            print("✅ Timeout handling test completed")
            return True
        except asyncio.TimeoutError:
            print("⏰ Timeout occurred (this is expected)")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    try:
        # Test with a timeout
        result = asyncio.run(asyncio.wait_for(timeout_test(), timeout=1.0))
        print("✅ Timeout test passed")
    except asyncio.TimeoutError:
        print("⏰ Timeout test triggered (this demonstrates the issue)")
    except Exception as e:
        print(f"❌ Timeout test failed: {e}")


def main():
    """Run diagnostics."""
    print("🩺 CLI HANGING DIAGNOSTIC TOOL")
    print("=" * 50)
    
    diagnose_api_key_issue()
    test_timeout_handling()
    
    print(f"\n🎯 SUMMARY:")
    print("The CLI hanging is likely due to:")
    print("1. Missing OPENROUTER_API_KEY causing HTTP client to hang")
    print("2. No timeout handling in the AI request flow")
    print("3. PydanticAI waiting indefinitely for API response")
    
    print(f"\n✅ IMMEDIATE FIXES:")
    print("1. Add API key validation before making requests")
    print("2. Add timeout handling to AI requests")
    print("3. Provide graceful fallback for offline mode")


if __name__ == "__main__":
    main()