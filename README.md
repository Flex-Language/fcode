# Flex AI Agent

A comprehensive AI-powered programming assistant for the Flex programming language with OpenRouter integration, providing access to 400+ AI models.

## 🚀 Features

- **Dual Syntax Support**: Works with both Franco Arabic and English Flex syntax
- **400+ AI Models**: Access to OpenRouter's extensive model catalog
- **Interactive Model Selection**: Browse, filter, and switch between models
- **Franco Loop Safety**: Critical validation for Franco l7d loop bounds
- **Code Generation**: AI-powered Flex code generation
- **Code Validation**: Comprehensive syntax and safety checking
- **Code Execution**: Direct Flex program execution with proper error handling
- **File Management**: Secure file operations with backup support
- **Interactive CLI**: Rich command-line interface with streaming responses

## ⚠️ Critical Safety Feature

**Franco l7d Loop Safety**: Franco loops are INCLUSIVE and will cause out-of-bounds errors if not handled correctly. The agent automatically validates and fixes:

```flex
// ❌ UNSAFE - Will cause out-of-bounds error!
karr i=0 l7d length(array) {
    print(array[i])  // ERROR on last iteration!
}

// ✅ SAFE - Proper Franco loop bounds
karr i=0 l7d length(array) - 1 {
    print(array[i])  // Safe access
}
```

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenRouter API key ([Get one here](https://openrouter.ai/keys))
- Flex CLI (if you want to execute Flex programs)

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd flex_code
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenRouter API key
   ```

4. **Validate installation**:
   ```bash
   python validate_implementation.py
   ```

## 🎯 Quick Start

### Interactive Mode

Start the interactive CLI:

```bash
python main.py
```

### Command Line Usage

```bash
# List available models
python main.py --models

# Generate code
python main.py --generate "create a Franco loop that prints numbers 1 to 10"

# Validate a Flex file
python main.py --validate examples/hello_world.flex

# Execute a Flex file
python main.py --execute examples/hello_world.flex
```

## 💻 CLI Commands

### Basic Commands
- `help` - Show help information
- `models` - Interactive model selection
- `switch <model_id>` - Switch to specific model
- `examples` - Show Flex code examples
- `clear` - Clear conversation history
- `exit` / `quit` - Exit application

### Programming Commands
- `validate <code>` - Validate Flex code
- `execute <code>` - Execute Flex code
- `/validate` - Interactive code validation
- `/execute` - Interactive code execution

### Utility Commands
- `settings` - Show current settings
- `history` - Show conversation history
- `save` - Save conversation to file

## 🔧 Configuration

### Environment Variables

```bash
# Required
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Optional
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
FLEX_CLI_PATH=flex
FLEX_EXAMPLES_DIR=./flex_examples
MAX_CODE_LENGTH=500
EXECUTION_TIMEOUT=30
DEFAULT_MODEL=anthropic/claude-3-5-sonnet
```

### Model Selection

The agent supports intelligent model selection based on:
- **Task complexity**: Simple tasks use cost-effective models
- **Feature requirements**: Complex tasks prefer models with tool support
- **Budget constraints**: Filter by cost per token
- **Context needs**: Filter by context window size

## 📁 Project Structure

```
flex_code/
├── agents/                    # AI agent components
│   ├── flex_agent.py         # Main Flex AI agent
│   ├── models.py             # Pydantic data models
│   └── providers.py          # OpenRouter provider config
├── tools/                     # Agent tools
│   ├── model_manager.py      # OpenRouter model management
│   ├── code_validator.py     # Flex code validation
│   ├── flex_executor.py      # Flex code execution
│   └── file_manager.py       # File operations
├── ui/                        # User interface
│   ├── cli.py                # Main CLI interface
│   ├── model_selector.py     # Interactive model selection
│   └── formatters.py         # Output formatting
├── config/                    # Configuration
│   └── settings.py           # Settings management
├── tests/                     # Unit tests
├── flex_examples/             # Example Flex programs
│   ├── franco_examples/      # Franco Arabic syntax
│   └── english_examples/     # English syntax
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=agents --cov=tools --cov=ui --cov-report=term-missing

# Run validation script
python validate_implementation.py
```

## 📝 Examples

### Franco Arabic Syntax

```flex
// Variables
rakm age = 25
klma name = "Ahmed"
so2al isStudent = sa7

// Function
sndo2 greet(klma personName) {
    etb3("Ahlan wa sahlan, " + personName + "!")
}

// Safe loop (CRITICAL: use length - 1)
dorg numbers = [1, 2, 3, 4, 5]
karr i=0 l7d length(numbers) - 1 {
    etb3("Number: " + numbers[i])
}

// Call function
greet(name)
```

### English Syntax

```flex
// Variables
int age = 25
string name = "John"
bool isStudent = true

// Function
fun greet(string personName) {
    print("Hello, " + personName + "!")
}

// Safe loop
list numbers = [1, 2, 3, 4, 5]
for(i=0; i<length(numbers); i++) {
    print("Number: " + numbers[i])
}

// Call function
greet(name)
```

## 🔍 Key Features

### Franco Loop Safety Validation

The agent includes comprehensive validation for Franco l7d loops:

- **Detection**: Automatically identifies unsafe loop patterns
- **Validation**: Warns about potential out-of-bounds errors
- **Auto-fixing**: Suggests and applies safe loop bounds
- **Examples**: Provides safe loop patterns

### Model Management

- **Caching**: Intelligent model metadata caching
- **Filtering**: Filter by cost, features, provider, context length
- **Suggestions**: AI-powered model recommendations
- **Switching**: Dynamic model switching during conversations

### Code Validation

- **Syntax checking**: Validates both Franco and English syntax
- **Safety analysis**: Checks for common programming errors
- **Style detection**: Automatically detects syntax style preference
- **Suggestions**: Provides improvement recommendations

## 🚨 Common Issues & Solutions

### Franco Loop Errors

**Problem**: Out-of-bounds array access
```flex
// This will crash!
karr i=0 l7d length(array) {
    print(array[i])  // ERROR!
}
```

**Solution**: Use proper bounds
```flex
// This is safe
karr i=0 l7d length(array) - 1 {
    print(array[i])  // Safe
}
```

### OpenRouter API Issues

- **Rate limits**: The agent includes automatic retry logic
- **Authentication**: Ensure your API key is valid and has credits
- **Model availability**: Some models may be temporarily unavailable

### Installation Issues

- **Python version**: Requires Python 3.8+
- **Dependencies**: Install all requirements with `pip install -r requirements.txt`
- **Environment**: Copy `.env.example` to `.env` and configure

## 🔗 Links

- [OpenRouter API Documentation](https://openrouter.ai/docs)
- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [Flex Language Specification](data/flex_language_spec.json)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 🆘 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Run the validation script: `python validate_implementation.py`
3. Check your `.env` configuration
4. Ensure you have sufficient OpenRouter credits
5. Open an issue with detailed error information

---

**Remember**: Franco l7d loops are INCLUSIVE! Always use `length(array) - 1` for safe array iteration.