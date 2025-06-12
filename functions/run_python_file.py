import os
import subprocess


def run_python_file(working_directory, file):
    cwd_abspath = os.path.abspath(working_directory)
    file_abspath = os.path.abspath(os.path.join(working_directory, file))

    if not file_abspath.startswith(cwd_abspath):
        return f'Error: Cannot execute "{file}" as it is outside the permitted working directory'
    if not os.path.exists(file_abspath):
        return f'Error: File "{file}" not found.'
    if not file_abspath.endswith(".py"):
        return f'Error: "{file}" is not a Python file.'

    try:
        process = subprocess.run(["python", file_abspath], capture_output=True, text=True, timeout=30)
        if process:
            output_str = f"Ran {file}\nSTDOUT: {process.stdout}\nSTDERR: {process.stderr}"
            if process.returncode != 0:
                output_str += f"\nProcess exited with code {process.returncode}"
        else:
            output_str = "No output produced"

        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
