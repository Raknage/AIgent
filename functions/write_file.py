import os


def write_file(working_directory, file, content):
    cwd_abspath = os.path.abspath(working_directory)
    file_abspath = os.path.abspath(os.path.join(working_directory, file))
    if not file_abspath.startswith(cwd_abspath):
        return f'Error: Cannot write to "{file}" as it is outside the permitted working directory'
    os.makedirs(os.path.dirname(file_abspath), exist_ok=True)

    if os.path.isdir(file_abspath):
        return f'Error: Cannot write to "{file}": it is a directory'

    with open(file_abspath, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file}" ({len(content)} characters written)'
