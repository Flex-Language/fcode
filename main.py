#!/usr/bin/env python3
"""
Main entry point for Flex AI Agent.

This script provides the primary entry point for the Flex AI Agent with
command-line argument support and proper error handling.
"""

import asyncio
import sys
import argparse
from pathlib import Path
from typing import Optional

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.cli import FlexCLI, main as cli_main
from config.settings import get_settings, validate_settings
from tools.model_manager import ModelManager
from agents.flex_agent import FlexAIAgent


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for CLI."""
    parser = argparse.ArgumentParser(
        description="Flex AI Agent - Interactive Programming Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Start interactive CLI
  python main.py --models           # Show available models
  python main.py --validate file.flex  # Validate Flex file
  python main.py --execute file.flex   # Execute Flex file
  python main.py --generate "create a loop"  # Generate code

For more help, run the interactive mode and type 'help'.
        """
    )
    
    # Mode selection (mutually exclusive)
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        '--interactive', '-i',
        action='store_true',
        default=True,
        help='Start interactive CLI mode (default)'
    )
    mode_group.add_argument(
        '--models', '-m',
        action='store_true',
        help='List available OpenRouter models'
    )
    mode_group.add_argument(
        '--validate', '-v',
        type=str,
        metavar='FILE',
        help='Validate a Flex file'
    )
    mode_group.add_argument(
        '--execute', '-e',
        type=str,
        metavar='FILE',
        help='Execute a Flex file'
    )
    mode_group.add_argument(
        '--generate', '-g',
        type=str,
        metavar='PROMPT',
        help='Generate Flex code from prompt'
    )
    
    # Model selection
    parser.add_argument(
        '--model',
        type=str,
        default=None,
        help='Specify OpenRouter model to use'
    )
    
    # Output options
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file for generated code'
    )
    
    # Syntax style
    parser.add_argument(
        '--syntax',
        choices=['franco', 'english', 'auto'],
        default='auto',
        help='Preferred syntax style (default: auto)'
    )
    
    # Debug options
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Flex AI Agent 1.0.0'
    )
    
    return parser


async def list_models() -> None:
    """List available OpenRouter models."""
    try:
        settings = get_settings()
        validate_settings(settings)
        
        print("📡 Loading available models...")
        model_manager = ModelManager(settings)
        models = await model_manager.list_models()
        
        if not models:
            print("❌ No models available.")
            return
        
        print(f"\n✅ Found {len(models)} available models:\n")
        
        for model in models[:20]:  # Show first 20
            prompt_price = model.pricing.get('prompt', 0)
            completion_price = model.pricing.get('completion', 0)
            
            print(f"• {model.name}")
            print(f"  ID: {model.id}")
            print(f"  Context: {model.context_length:,} tokens")
            print(f"  Price: ${prompt_price:.6f}/prompt, ${completion_price:.6f}/completion")
            
            if model.description:
                desc = model.description[:100] + "..." if len(model.description) > 100 else model.description
                print(f"  Description: {desc}")
            print()
        
        if len(models) > 20:
            print(f"... and {len(models) - 20} more models.")
            print("Use interactive mode for full model browser.")
    
    except Exception as e:
        print(f"❌ Error loading models: {e}")
        sys.exit(1)


async def validate_file(filepath: str) -> None:
    """Validate a Flex file."""
    try:
        settings = get_settings()
        validate_settings(settings)
        
        # Read file
        file_path = Path(filepath)
        if not file_path.exists():
            print(f"❌ File not found: {filepath}")
            sys.exit(1)
        
        code = file_path.read_text(encoding='utf-8')
        
        # Initialize agent
        agent = FlexAIAgent(settings)
        
        print(f"🔍 Validating {filepath}...")
        result = await agent.run(f"validate this Flex code:\n```flex\n{code}\n```")
        print(result)
    
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        sys.exit(1)


async def execute_file(filepath: str) -> None:
    """Execute a Flex file."""
    try:
        settings = get_settings()
        validate_settings(settings)
        
        # Read file
        file_path = Path(filepath)
        if not file_path.exists():
            print(f"❌ File not found: {filepath}")
            sys.exit(1)
        
        code = file_path.read_text(encoding='utf-8')
        
        # Initialize agent
        agent = FlexAIAgent(settings)
        
        print(f"🚀 Executing {filepath}...")
        result = await agent.run(f"execute this Flex code:\n```flex\n{code}\n```")
        print(result)
    
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        sys.exit(1)


async def generate_code(prompt: str, syntax: str = 'auto', output_file: Optional[str] = None) -> None:
    """Generate Flex code from prompt."""
    try:
        settings = get_settings()
        validate_settings(settings)
        
        # Initialize agent
        agent = FlexAIAgent(settings)
        
        print(f"🤖 Generating Flex code for: {prompt}")
        if syntax != 'auto':
            prompt_with_syntax = f"Generate Flex code using {syntax} syntax: {prompt}"
        else:
            prompt_with_syntax = f"Generate Flex code: {prompt}"
        
        result = await agent.run(prompt_with_syntax)
        print(result)
        
        # Save to file if requested
        if output_file:
            try:
                # Extract code from result (look for ```flex blocks)
                import re
                code_match = re.search(r'```flex\n(.*?)\n```', result, re.DOTALL)
                if code_match:
                    code = code_match.group(1)
                    Path(output_file).write_text(code, encoding='utf-8')
                    print(f"\n💾 Code saved to {output_file}")
                else:
                    print("\n⚠️ Could not extract code block for saving")
            except Exception as e:
                print(f"\n❌ Failed to save to file: {e}")
    
    except Exception as e:
        print(f"❌ Code generation failed: {e}")
        sys.exit(1)


async def main() -> None:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set up debug mode
    if args.debug:
        import logging
        logging.basicConfig(level=logging.DEBUG)
    
    try:
        # Handle different modes
        if args.models:
            await list_models()
        
        elif args.validate:
            await validate_file(args.validate)
        
        elif args.execute:
            await execute_file(args.execute)
        
        elif args.generate:
            await generate_code(args.generate, args.syntax, args.output)
        
        else:
            # Default to interactive mode
            print("🚀 Starting Flex AI Agent in interactive mode...")
            print("Use --help for command-line options.\n")
            
            # Override model if specified
            if args.model:
                try:
                    settings = get_settings()
                    validate_settings(settings)
                    agent = FlexAIAgent(settings)
                    await agent.switch_model(args.model)
                    print(f"✅ Using model: {args.model}\n")
                except Exception as e:
                    print(f"⚠️ Warning: Could not switch to model {args.model}: {e}")
                    print("Using default model.\n")
            
            await cli_main()
    
    except KeyboardInterrupt:
        # Clean exit - no error message needed since CLI handles it
        pass
    except asyncio.CancelledError:
        # Clean exit for cancelled async operations
        pass
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Ensure we're using the right Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required.")
        sys.exit(1)
    
    # Check for required environment
    try:
        get_settings()
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        print("\nPlease ensure your .env file is set up correctly.")
        print("Copy .env.example to .env and fill in your OpenRouter API key.")
        sys.exit(1)
    
    # Run with proper cancellation handling
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Clean exit for Ctrl+C
        pass
    except asyncio.CancelledError:
        # Clean exit for cancelled operations
        pass
    except SystemExit:
        pass  # Let system exits pass through normally