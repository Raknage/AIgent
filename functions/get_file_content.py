import os

MAX_CHARS = 10000


def get_file_content(working_directory, file_path):
    try:
        cwd_abspath = os.path.abspath(working_directory)
        file_abspath = os.path.abspath(os.path.join(working_directory, file_path))
        if not os.path.isfile(file_abspath):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        if not file_abspath.startswith(cwd_abspath):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(file_abspath, "r") as f:
            file_content_string = f.read(MAX_CHARS)
        if len(file_content_string) >= MAX_CHARS:
            file_content_string += (
                f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            )

        return file_content_string
    except Exception as e:
        return f"error: {e}"
