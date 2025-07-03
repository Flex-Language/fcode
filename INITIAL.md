## FEATURE:
Build an AI agent that understands and generates code for the Flex programming language, leveraging the comprehensive language specification in `data/flex_language_spec.json`. The agent should:
- Generate Flex source files and Bash scripts.
- Execute Flex files via the CLI (`flex {flex file}` command).
- Read and write files from the filesystem.
- Interact with users through a CLI interface.
- Use the Flex language spec as its core knowledge base for code generation, error handling, and best practices.
- Integrate with https://openrouter.ai/ to allow the user to choose from all available AI models for code generation and assistance.
- Provide a way for users to list, search, and filter available models from OpenRouter, making model selection easy and flexible.

## EXAMPLES:
- No examples are currently available for this project.

## DOCUMENTATION:
- `data/flex_language_spec.json` — Full Flex language specification (syntax, patterns, error handling, best practices).
- `codefetch/codebase.md` — Project structure, conventions, and meta-guidelines.
- Flex CLI usage: `flex {filename}` to execute Flex files.
- Example Flex programs and patterns from the language spec.

## OTHER CONSIDERATIONS:
- The agent must always use the Flex language spec for code generation and error explanations.
- All generated code must follow Flex best practices (no semicolons, safe loop bounds, mixed syntax support, etc.).
- The agent should validate user input and provide clear error messages.
- CLI should support commands for generating, running, and reading files.
- Ensure no sensitive data is written to disk.
- Modularize code for easy extension (e.g., future support for more languages or tools).
- Add unit tests for all major features (file generation, execution, error handling).
- The agent should support model selection from all models available via https://openrouter.ai/, including listing, searching, and filtering models for user convenience.
