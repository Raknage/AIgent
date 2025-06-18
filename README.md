
# AI Coding Agent

This project is an AI coding agent that uses the Gemini API to interact with the file system. It can list files and directories, read file contents, write or overwrite files, and execute Python files.

This was a boot.dev project. Learn more at [boot.dev](https://boot.dev).

## Features

*   **List files and directories:** Uses the `get_file_info` function to list files in a specified directory along with their sizes.
*   **Read file contents:** Uses the `get_file_content` function to read the content of a file.
*   **Write files:** Uses the `write_file` function to write content to a file.
*   **Run Python files:** Uses the `run_python_file` function to execute a Python file.

## Dependencies

*   google-genai
*   python-dotenv

## Usage

1.  Set the `GEMINI_API_KEY` environment variable.
2.  Run `main.py` with a prompt as a command-line argument:

    ```bash
    python main.py "List files in the current directory"
    ```

3. Use `--verbose` argument for more informative output

    ```bash
    python main.py "prompt" --verbose
    ```

## Project Structure

*   `main.py`: Main entry point of the application. Defines the AI agent and handles user input.
*   `functions/`: Contains the implementation of the file system interaction functions.
    *   `get_file_info.py`: Implements the `get_file_info` function.
    *   `get_file_content.py`: Implements the `get_file_content` function.
    *   `write_file.py`: Implements the `write_file` function.
    *   `run_python_file.py`: Implements the `run_python_file` function.
*   `requirements.txt`: Contains the project dependencies.
*   `tests.py`: Contains tests for all the functions.
*   `calculator/`: Not included. Was used to test initially.

### This file was (mostly) generated with this very program