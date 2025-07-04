#!/usr/bin/env python3
"""
Test the CLI exit functionality (should exit cleanly without errors)
"""

import asyncio
import signal
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.cli import FlexCLI


async def test_clean_exit():
    """Test that the CLI exits cleanly."""
    print("🧪 Testing clean exit functionality...")
    
    try:
        cli = FlexCLI()
        
        # Simulate initialization
        await cli._initialize_components()
        
        # Test the exit command
        await cli._exit_command()
        
        if not cli.is_running:
            print("✅ Exit command sets is_running to False correctly")
            return True
        else:
            print("❌ Exit command failed to set is_running to False")
            return False
            
    except Exception as e:
        print(f"❌ Exit test failed: {e}")
        return False


async def main():
    """Run the exit test."""
    print("🚀 Testing CLI exit functionality...\n")
    
    success = await test_clean_exit()
    
    if success:
        print("✅ Exit functionality test passed!")
    else:
        print("❌ Exit functionality test failed!")


if __name__ == "__main__":
    asyncio.run(main())
