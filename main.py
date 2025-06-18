import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions import get_file_content, get_file_info, write_file, run_python_file


def main():
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    schema_get_file_info = types.FunctionDeclaration(
        name="get_file_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )
    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Read the content of a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="File to read the content from",
                ),
            },
        ),
    )
    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Run a python file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="Python file to run",
                ),
            },
        ),
    )
    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Write string to a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file": types.Schema(
                    type=types.Type.STRING,
                    description="File to write to",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="content to write to the file",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_file_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    try:
        prompt = sys.argv[1]
    except IndexError:
        print("Usage: main.py [prompt]")
        exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    model = "gemini-2.0-flash-001"
    config = types.GenerateContentConfig(
        system_instruction=system_prompt, tools=[available_functions]
    )

    response = client.models.generate_content(
        model=model, contents=messages, config=config
    )

    if response.function_calls:
        for function_call_part in response.function_calls[0]:
            function_call_result = call_function(function_call_part)
            if function_call_result.parts[0].function_response.response:
                if "--verbose" in sys.argv:
                    print(
                        f"-> {function_call_result.parts[0].function_response.response}"
                    )
            else:
                raise BaseException("Error: function call failed")
    else:
        print(response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    cwd = "./calculator"
    args = function_call_part.function_call.args
    args["working_directory"] = cwd

    if verbose:
        print(f"Calling function: {function_call_part.name}({args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    match function_call_part.name:
        case "get_file_info":
            function_result = get_file_info.get_file_info(**args)
        case "get_file_content":
            function_result = get_file_content.get_file_content(**args)
        case "write_file":
            function_result = write_file.write_file(**args)
        case "run_python_file":
            function_result = run_python_file.run_python_file(**args)
        case _:
            return types.Content(
                role="tool",
                parts=[
                    types.Part.from_function_response(
                        name=function_call_part.name,
                        response={
                            "error": f"Unknown function: {function_call_part.name}"
                        },
                    )
                ],
            )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_result},
            )
        ],
    )


main()
