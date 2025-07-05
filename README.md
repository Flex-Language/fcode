# 🚀 Flex AI Agent with OpenRouter Integration

A comprehensive AI-powered programming assistant for the Flex programming language, featuring **400+ AI models** from OpenRouter, intelligent code generation, and advanced CLI interface.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-400%2B%20Models-brightgreen)](https://openrouter.ai/)
[![Flex Language](https://img.shields.io/badge/Flex-Franco%20%7C%20English-orange)](https://github.com/flex-lang)

## ✨ Features

### 🧠 **Advanced AI Integration**
- **400+ AI Models** via OpenRouter.ai (Claude, GPT-4, Llama, Qwen, and more)
- **Dynamic Model Switching** - Choose the best model for your task
- **Intelligent Model Selection** - Get recommendations based on task complexity
- **Cost Optimization** - Filter models by price and features

### 🔧 **Flex Programming Language Support**
- **Dual Syntax Support** - Franco Arabic (`karr`, `etb3`, `l7d`) and English (`for`, `print`, `while`)
- **Franco Loop Safety** - Automatic detection and correction of inclusive loop bounds
- **Syntax Detection** - Automatically identifies and adapts to your preferred style
- **Code Validation** - Real-time validation against Flex language specification

### 💻 **Interactive CLI Experience**
- **Rich Terminal UI** - Beautiful, responsive interface with syntax highlighting
- **Interactive Model Browser** - Browse, search, and filter 400+ models
- **Real-time Code Execution** - Execute Flex programs directly from the CLI
- **Conversation History** - Persistent context across your programming session
- **Smart Command System** - Intuitive commands for all operations

### 🛡️ **Enterprise-Ready Features**
- **Comprehensive Error Handling** - Graceful failure recovery and detailed error messages
- **Security Validation** - File operation security and input sanitization
- **Performance Monitoring** - Model usage metrics and cost tracking
- **Async Architecture** - Non-blocking operations for responsive experience
- **Extensive Testing** - 85%+ test coverage with comprehensive test suite

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.8 or higher**
- **OpenRouter API Key** (get one free at [openrouter.ai](https://openrouter.ai/keys))
- **Flex CLI** (optional, for code execution)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/your-username/flex-ai-agent.git
cd flex-ai-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your OpenRouter API key
nano .env  # or your preferred editor
```

**Required in `.env`:**
```bash
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### 3. Launch the Agent

```bash
python main.py
```

🎉 **You're ready to code with AI assistance!**

---

## 📖 Usage Guide

### Interactive CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `help` | Show help information | `help` |
| `models` | Interactive model selection | `models` |
| `switch <model>` | Switch to specific model | `switch anthropic/claude-3-5-sonnet` |
| `examples` | Show Flex code examples | `examples` |
| `validate <code>` | Validate Flex code | `validate "etb3('hello')"` |
| `execute <code>` | Execute Flex code | `execute "karr i=0 l7d 9 { etb3(i) }"` |
| `clear` | Clear conversation history | `clear` |
| `history` | Show conversation history | `history` |
| `settings` | Show current settings | `settings` |
| `exit` / `quit` | Exit application | `exit` |

### Programming with Franco Syntax

**Franco Arabic syntax** uses culturally familiar keywords:

```flex
// Variables
rakm number = 42          // Integer
kasr decimal = 3.14       // Float  
klma text = "Marhaba"     // String
so2al flag = sa7          // Boolean (sa7=true, ghalt=false)
dorg list = [1, 2, 3]     // Array

// Safe Franco loops (CRITICAL: notice the -1 for safety)
karr i=0 l7d length(list) - 1 {
    etb3("Item " + i + ": " + list[i])
}

// Conditionals
lw number > 10 yalla
    etb3("Number is greater than 10")
gher yalla
    etb3("Number is 10 or less")
safi

// Functions
sndo2 greet(klma name) {
    etb3("Ahlan wa sahlan, " + name + "!")
}

greet("Ahmed")
```

### Programming with English Syntax

**English syntax** follows familiar programming conventions:

```flex
// Variables
int number = 42
float decimal = 3.14
string text = "Hello"
bool flag = true
list array = [1, 2, 3]

// Standard loops
for(i=0; i<length(array); i++) {
    print("Item " + i + ": " + array[i])
}

// Conditionals
if(number > 10) {
    print("Number is greater than 10")
} else {
    print("Number is 10 or less")
}

// Functions
fun greet(string name) {
    print("Hello, " + name + "!")
}

greet("Alice")
```

### Model Selection

**Choose from 400+ models** based on your needs:

```bash
# Interactive model browser
> models
📋 Loading available models...
[Interactive selection menu appears]

# Direct model switching
> switch anthropic/claude-3-5-sonnet
✅ Switched to model: anthropic/claude-3-5-sonnet

# Get model recommendations
> models
⭐ Recommended Models for Flex Programming
```

**Model Categories:**
- **Free Models**: `qwen/qwen-14b:free`, `meta-llama/llama-3.1-8b-instruct:free`
- **Balanced**: `anthropic/claude-3-5-haiku`, `openai/gpt-4o-mini`
- **Premium**: `anthropic/claude-3-5-sonnet`, `openai/gpt-4o`
- **Specialized**: `deepseek/deepseek-coder`, `meta-llama/codellama-70b-instruct`

---

## 🔧 Advanced Configuration

### Environment Variables

Create a `.env` file with these options:

```bash
# === OpenRouter Configuration ===
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_HTTP_REFERER=https://github.com/your-repo
OPENROUTER_APP_TITLE=Flex AI Agent

# === Flex Language Settings ===
FLEX_CLI_PATH=flex
FLEX_EXAMPLES_DIR=./flex_examples
FLEX_TEMP_DIR=./temp
FLEX_FILE_EXTENSIONS=.flex,.flx

# === Application Settings ===
MAX_CODE_LENGTH=500
EXECUTION_TIMEOUT=30
ENABLE_FILE_OPERATIONS=true
MODEL_CACHE_DURATION=3600
DEFAULT_MODEL=anthropic/claude-3-5-sonnet

# === Cost Optimization ===
ENABLE_COST_OPTIMIZATION=true
DAILY_BUDGET_LIMIT=10.0
PREFER_FREE_MODELS=false

# === Development ===
DEBUG=false
LOG_LEVEL=INFO
ENABLE_METRICS=false
```

### Command Line Options

```bash
# Start interactive mode (default)
python main.py

# Show available models
python main.py --models

# Validate a Flex file
python main.py --validate examples/hello_world.flex

# Execute a Flex file
python main.py --execute examples/hello_world.flex

# Generate code from command line
python main.py --generate "create a Franco loop that prints numbers 1 to 10"

# Show help
python main.py --help
```

---

## 📚 Example Interactions

### Code Generation

```bash
> generate a safe Franco loop that prints array elements

🤖 Assistant: I'll create a safe Franco loop for you. Notice the crucial `- 1` 
to prevent out-of-bounds errors since Franco loops are INCLUSIVE.

```flex
// Safe Franco array iteration
dorg myArray = ["apple", "banana", "cherry", "date"]

karr i=0 l7d length(myArray) - 1 {
    etb3("Element " + i + ": " + myArray[i])
}
```

✅ This is safe because Franco `l7d` loops are inclusive, so using 
`length(myArray) - 1` ensures we don't exceed array bounds.
```

### Error Detection and Fixing

```bash
> validate this code: karr i=0 l7d length(arr) { etb3(arr[i]) }

🤖 Assistant: ❌ Code validation failed

**Critical Franco Loop Safety Error:**
- Line 1: Franco l7d loop will cause out-of-bounds access
- Fix: Change `l7d length(arr)` to `l7d length(arr) - 1`
- Reason: Franco loops are INCLUSIVE - they run from start TO end (including end)

**Corrected code:**
```flex
karr i=0 l7d length(arr) - 1 {
    etb3(arr[i])
}
```
```

### Model Switching

```bash
> switch to a cost-effective model for simple tasks

🤖 Assistant: I'll help you switch to a cost-effective model perfect for simple tasks.

📋 Cost-Effective Models:
• qwen/qwen-14b:free - FREE, great for basic code generation
• meta-llama/llama-3.1-8b-instruct:free - FREE, good for explanations  
• anthropic/claude-3-5-haiku - $0.00025/1K tokens, fast and efficient

> switch qwen/qwen-14b:free
✅ Switched to model: qwen/qwen-14b:free

This model is perfect for:
- Simple code generation
- Basic debugging help
- Learning Flex syntax
- Cost-conscious development
```

---

## 🏗️ Project Structure

```
flex_code/
├── agents/                    # AI agent components
│   ├── __init__.py           # Package initialization
│   ├── flex_agent.py         # Main Flex AI agent
│   ├── models.py             # Pydantic data models
│   └── providers.py          # OpenRouter provider config
├── tools/                     # Agent tools
│   ├── __init__.py           # Package initialization
│   ├── model_manager.py      # OpenRouter model management
│   ├── flex_executor.py      # Flex code execution
│   ├── file_manager.py       # File operations
│   └── code_validator.py     # Flex code validation
├── ui/                        # User interface
│   ├── __init__.py           # Package initialization
│   ├── cli.py                # Main CLI interface
│   ├── model_selector.py     # Interactive model selection
│   └── formatters.py         # Output formatting
├── config/                    # Configuration
│   ├── __init__.py           # Package initialization
│   └── settings.py           # Settings management
├── tests/                     # Test suite (85%+ coverage)
│   ├── test_flex_agent.py    # Agent tests
│   ├── test_model_manager.py # Model management tests
│   ├── test_file_manager.py  # File operation tests
│   ├── test_code_validator.py# Validation tests
│   ├── test_flex_executor.py # Execution tests
│   ├── test_model_selector.py# UI tests
│   └── test_cli.py           # CLI tests
├── flex_examples/             # Example Flex programs
│   ├── franco_examples/      # Franco syntax examples
│   │   ├── hello_world.flex  # Basic Franco example
│   │   ├── safe_loops.flex   # Franco loop safety demo
│   │   └── advanced_patterns.flex # Complex patterns
│   └── english_examples/     # English syntax examples
│       ├── hello_world.flex  # Basic English example
│       └── advanced_algorithms.flex # Advanced algorithms
├── cache/                     # Model cache
│   └── models_cache.json     # Cached model information
├── data/                      # Language specifications
│   └── flex_language_spec.json # Complete Flex spec
├── main.py                    # Entry point
├── requirements.txt           # Python dependencies
├── .env.example              # Environment template
└── README.md                 # This file
```

---

## 🧪 Development & Testing

### Running Tests

```bash
# Run all tests with coverage
pytest tests/ -v --cov=agents --cov=tools --cov=ui --cov-report=term-missing

# Run specific test categories
pytest tests/test_flex_agent.py -v
pytest tests/test_model_manager.py -v
pytest tests/test_code_validator.py -v

# Run tests with detailed output
pytest tests/ -v -s
```

### Code Quality

```bash
# Format code
black .

# Lint code
ruff check . --fix

# Type checking
mypy .

# Security scanning
bandit -r .
```

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run pre-commit checks
pre-commit run --all-files
```

---

## 🚨 Troubleshooting

### Common Issues

#### ❌ "Invalid OpenRouter API key"
**Solution:**
1. Check your `.env` file contains: `OPENROUTER_API_KEY=your_actual_key`
2. Verify your API key at [openrouter.ai/keys](https://openrouter.ai/keys)
3. Ensure you have sufficient credits

#### ❌ "Flex CLI not found"
**Solution:**
1. Install Flex CLI: `npm install -g flex-cli` (or your system's method)
2. Set custom path: `FLEX_CLI_PATH=/path/to/flex` in `.env`
3. Disable execution: `ENABLE_FILE_OPERATIONS=false` in `.env`

#### ❌ "No models available"
**Solution:**
1. Check internet connection
2. Verify API key permissions
3. Try refreshing: Type `models` in CLI and select "Refresh model cache"

#### ❌ "Franco loop safety errors"
**This is intentional!** Franco loops are inclusive. Always use:
```flex
// ✅ SAFE: Use length - 1
karr i=0 l7d length(array) - 1 { ... }

// ❌ UNSAFE: Will cause out-of-bounds
karr i=0 l7d length(array) { ... }
```

#### ❌ "Rate limit exceeded"
**Solution:**
1. Use free models: `qwen/qwen-14b:free` or `meta-llama/llama-3.1-8b-instruct:free`
2. Enable cost optimization: `ENABLE_COST_OPTIMIZATION=true`
3. Set budget limit: `DAILY_BUDGET_LIMIT=5.0`

### Debug Mode

Enable debug mode for detailed logging:

```bash
# In .env file
DEBUG=true
LOG_LEVEL=DEBUG
ENABLE_METRICS=true
```

### Performance Issues

```bash
# Reduce model cache duration
MODEL_CACHE_DURATION=1800  # 30 minutes

# Disable file operations
ENABLE_FILE_OPERATIONS=false

# Use faster models
DEFAULT_MODEL=anthropic/claude-3-5-haiku
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md).

### Quick Contribution Steps

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Development Priorities

- 🔧 **New Model Integrations** - Add support for more AI providers
- 🚀 **Flex Language Features** - Enhanced syntax support and validation
- 💻 **UI Improvements** - Better CLI experience and formatting
- 🧪 **Testing** - Increase test coverage and add integration tests
- 📚 **Documentation** - More examples and tutorials

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[OpenRouter](https://openrouter.ai/)** - For providing access to 400+ AI models
- **[PydanticAI](https://ai.pydantic.dev/)** - For the excellent AI agent framework
- **[Rich](https://rich.readthedocs.io/)** - For beautiful terminal interfaces
- **[Flex Language](https://github.com/flex-lang)** - For the innovative dual-syntax programming language

---

## 📞 Support

- **📖 Documentation**: [Full Documentation](https://your-docs-url.com)
- **💬 Discussions**: [GitHub Discussions](https://github.com/your-username/flex-ai-agent/discussions)
- **🐛 Issues**: [GitHub Issues](https://github.com/your-username/flex-ai-agent/issues)
- **📧 Email**: support@your-domain.com

---

## 🚀 What's Next?

- **🔮 Multi-Agent Systems** - Collaborative AI agents for complex projects
- **🌐 Web Interface** - Browser-based IDE with real-time collaboration  
- **📱 Mobile Support** - Native mobile apps for on-the-go coding
- **🎓 Learning Mode** - Interactive tutorials and guided programming lessons
- **🔗 IDE Integration** - VS Code, IntelliJ, and other IDE plugins

---

<div align="center">

**Made with ❤️ by the Flex AI Agent Team**

[⭐ Star this project](https://github.com/your-username/flex-ai-agent) | [🍴 Fork it](https://github.com/your-username/flex-ai-agent/fork) | [📖 Read the docs](https://your-docs-url.com)

*Empowering developers with AI-assisted Flex programming*

</div>