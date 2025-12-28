# AI Coding Agent

An intelligent CLI tool powered by Google's Gemini AI that can autonomously interact with your codebase, analyze files, run Python scripts, and make modifications.

## Features

- **File Analysis**: List and inspect files and directories
- **Code Execution**: Run Python files and capture output
- **File Operations**: Read and write files with security controls
- **AI-Powered**: Uses Google Gemini to understand natural language commands
- **Interactive**: Supports up to 20 iterations of tool calls for complex tasks
- **Secure**: Built-in path traversal protection

## Prerequisites

- Python 3.7 or higher
- Google Gemini API key

## Installation

1. Clone this repository:
```bash
git clone https://github.com/YOUR_USERNAME/Coding_Agent.git
cd Coding_Agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory:
```
GEMINI_API_KEY=your_api_key_here
WORKING_DIR=./calculator
MAX_CHARS=1000
```

Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Usage

Run the tool with a natural language prompt:

```bash
python main.py "your command here"
```

### Examples

```bash
# List files in a directory
python main.py "List all Python files in the calculator directory"

# Read and analyze code
python main.py "What does the Calculator class do?"

# Run tests
python main.py "Run the test file and show me the results"

# Modify code
python main.py "Add a new method to handle division by zero"

# Fix and debug applications
python main.py "fix my calculator app, it's not starting correctly"

# Verbose mode for debugging
python main.py "Analyze the calculator implementation" --verbose
```

### Example: Fixing a Calculator App

```bash
> python main.py "fix my calculator app, it's not starting correctly"
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Calling function: write_file
# Calling function: run_python_file
# Final response:
# Great! The calculator app now seems to be working correctly. The output shows the expression and the result in a formatted way.
```

This example demonstrates how the AI agent autonomously:
1. Inspects the project files to understand the structure
2. Reads the relevant source code to identify the issue
3. Fixes the code by writing the corrected file
4. Runs the application to verify the fix works
5. Iterates if needed until the problem is resolved

## Project Structure

```
Coding_Agent/
├── main.py                 # Entry point and conversation loop
├── call_function.py        # Function orchestration and tool definitions
├── config.py              # Configuration (working directory, API key)
├── prompts.py             # System prompt for the AI agent
├── functions/             # Available tool implementations
│   ├── get_files_info.py  # List files and directories
│   ├── get_file_content.py # Read file contents
│   ├── run_python_file.py  # Execute Python scripts
│   └── write_file.py       # Write/modify files
├── calculator/            # Example project for testing
│   ├── main.py
│   ├── test.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
└── tests/                 # Unit tests for functions
```

## Available Functions

The AI agent has access to these tools:

1. **get_files_info**: Lists files and directories with details (size, type, modification time)
2. **get_file_content**: Reads file contents (configurable character limit)
3. **run_python_file**: Executes Python files and captures stdout/stderr
4. **write_file**: Creates or modifies files

## Configuration

Edit [config.py](config.py) to customize:

- `WORKING_DIR`: Directory the agent operates in (default: `./calculator`)
- `MAX_CHARS`: Maximum characters to read from files (default: `1000`)
- `GEMINI_API_KEY`: Loaded from `.env` file

## Security

- All file operations are restricted to the `WORKING_DIR` to prevent path traversal attacks
- The `.env` file containing your API key is excluded from git via `.gitignore`
- File content reading is limited to prevent memory issues

## Example Use Cases

- **Code Review**: "Review the calculator implementation for potential bugs"
- **Testing**: "Run all tests and analyze any failures"
- **Documentation**: "Generate docstrings for all functions in calculator.py"
- **Refactoring**: "Improve error handling in the Calculator class"
- **Analysis**: "How does the calculator render results to the console?"
- **Debugging**: "Fix my calculator app, it's not starting correctly"

## Limitations

- Maximum 20 iterations per conversation to prevent infinite loops
- File reading limited by `MAX_CHARS` configuration
- Only Python file execution is supported
- Operations restricted to `WORKING_DIR`

## Development

To run the tests:

```bash
python test_files_info.py
python test_file_content.py
python test_run_python_file.py
python test_write_file.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Powered by [Google Gemini API](https://ai.google.dev/)
- Built with Python 3

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
