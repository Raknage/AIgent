import os
import sys
import json
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

    You have only 20 iterations to accomplish this task.
    All paths you provide should be relative to the working directory. Do not specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    schema_get_file_info = types.FunctionDeclaration(
        name="get_file_info",
        description="Lists files in the specified directory along with their sizes.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from. Provide empty string to list files in the working directory itself.",
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
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Path to the file to read the content from",
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
        if "--verbose" in sys.argv:
            verbose = True
        else:
            verbose = False
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

    for i in range(20):
        response = client.models.generate_content(
            model=model, contents=messages, config=config
        )
        for candidate in response.candidates:
            messages.append(candidate.content)

        if verbose and candidate.content.parts[0].text:
            print(candidate.content.parts[0].text)

        if response.function_calls:
            for function_call_part in response.function_calls:
                function_call_result = call_function(function_call_part, verbose)
                messages.append(function_call_result)

                if function_call_result.parts[0].function_response.response:
                    if verbose:
                        print(
                            f"-> {function_call_result.parts[0].function_response.response}"
                        )
                else:
                    raise BaseException("Error: function call failed")

        elif i >= 20:
            print(response.text, f"iteration: {i}")
            break
        else:
            print(response.text)
            break

    write_file.write_file(".", "messages.py", "".join(str(messages)))
    if verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


def call_function(function_call_part, verbose=False):
    cwd = "./calculator"
    args = function_call_part.args
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
