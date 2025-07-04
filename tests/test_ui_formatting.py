#!/usr/bin/env python3
"""
Test the enhanced UI formatting with Rich markup.
"""

import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui import formatters

def test_ui_formatting():
    """Test enhanced UI formatting functions."""
    print("🎨 Testing Enhanced UI Formatting")
    print("=" * 60)
    
    # Test enhanced response display
    sample_response = """Here's a simple Flex program:

```flex
// Franco syntax example
rakm counter = 0
karr i=0 l7d 4 {
    etb3("Count: " + i)
    counter = counter + 1
}
etb3("Final counter: " + counter)
```

This program safely iterates from 0 to 4 using Franco syntax."""
    
    print("Testing enhanced AI response formatting:")
    formatters.display_enhanced_ai_response(sample_response, "claude-3.5-sonnet")
    
    print("\n" + "=" * 60)
    print("🎯 UI Formatting Test Complete!")

if __name__ == "__main__":
    test_ui_formatting()