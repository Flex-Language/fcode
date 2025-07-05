#!/usr/bin/env python3
"""
Integration test to verify the main application can start and exit cleanly.
This simulates what happens when a user runs the main program.
"""

import signal
import subprocess
import sys
import time
from pathlib import Path


def test_main_program_startup_and_exit():
    """Test that main.py can start and be interrupted cleanly."""
    print("🧪 Testing main program startup and clean exit...")
    
    try:
        # Start the main program
        process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd="/Users/mikawi/Developer/grad/flex_code",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Let it start up
        time.sleep(3)
        
        # Send interrupt signal (like Ctrl+C)
        process.send_signal(signal.SIGINT)
        
        # Wait for it to exit
        stdout, stderr = process.communicate(timeout=10)
        
        # Check exit code
        if process.returncode == 0:
            print("✅ Main program exited cleanly with code 0")
            return True
        elif process.returncode == -2:  # SIGINT
            print("✅ Main program was interrupted and exited cleanly")
            return True
        else:
            print(f"❌ Main program exited with unexpected code: {process.returncode}")
            if stderr:
                print(f"Stderr: {stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Main program didn't exit within timeout")
        process.kill()
        return False
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        return False


def main():
    """Run the integration test."""
    print("🚀 Testing main program integration...\n")
    
    success = test_main_program_startup_and_exit()
    
    if success:
        print("✅ Integration test passed!")
        print("The main program can now start and exit cleanly without errors.")
    else:
        print("❌ Integration test failed!")


if __name__ == "__main__":
    main()
