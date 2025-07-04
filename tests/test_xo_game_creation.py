#!/usr/bin/env python3
"""
Test script to verify the XO game creation works exactly like the user's scenario.
"""

import asyncio
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.flex_agent import FlexAIAgent
from config.settings import get_settings

async def test_xo_game_creation():
    """Test the exact scenario the user was experiencing."""
    print("🎮 Testing XO Game Creation (User Scenario)")
    print("=" * 60)
    
    # Initialize agent
    settings = get_settings()
    agent = FlexAIAgent(settings)
    
    print("Step 1: User asks for XO game code")
    response1 = await agent.run("try to code xo game using flex")
    print("✅ Generated XO game code")
    
    print("\nStep 2: User asks to create a file")
    response2 = await agent.run("create a file using this code")
    print("Agent Response:")
    print(response2[:200] + "..." if len(response2) > 200 else response2)
    
    print("\nStep 3: User provides specific filename and syntax")
    response3 = await agent.run("filename would be xo_game.lx the code you just wrote and code could be franco")
    print("Agent Response:")
    print(response3[:300] + "..." if len(response3) > 300 else response3)
    
    # Check if file was created
    if os.path.exists("xo_game.lx"):
        print("\n✅ SUCCESS: File 'xo_game.lx' was created!")
        with open("xo_game.lx", "r") as f:
            content = f.read()
        print(f"\nFile size: {len(content)} characters")
        print("File contents preview:")
        print(content[:400] + "..." if len(content) > 400 else content)
        
        # Clean up
        os.remove("xo_game.lx") 
        print("\n🧹 Test file cleaned up.")
    else:
        print("\n❌ ISSUE: File 'xo_game.lx' was not created.")
        print("The agent needs to actually call the create_file or create_flex_program_file tool!")
    
    print("\n" + "=" * 60)
    print("🎯 XO Game Creation Test Complete!")

if __name__ == "__main__":
    asyncio.run(test_xo_game_creation())