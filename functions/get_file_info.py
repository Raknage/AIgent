import os


def get_file_info(working_directory: str, directory: str = None):
    cwd_abspath = os.path.abspath(working_directory)
    dir_abspath = os.path.abspath(os.path.join(working_directory, directory))
    abs_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not os.path.isdir(abs_dir):
        return f'Error: "{directory}" is not a directory'
    if not dir_abspath.startswith(cwd_abspath):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    list_of_strings = []
    files = os.listdir(abs_dir)

    for file in files:
        file_path = os.path.join(abs_dir, file)
        is_dir = os.path.isdir(file_path)
        if is_dir:
            size = get_folder_size(file_path)
        else:
            size = os.path.getsize(file_path)
        list_of_strings.append(f"- {file}: file_size={size} bytes, is_dir={is_dir}")

    return "\n".join(list_of_strings)


def get_folder_size(folder_path):
    total_size = 0
    with os.scandir(folder_path) as it:
        for entry in it:
            if entry.is_file():
                total_size += entry.stat().st_size
            elif entry.is_dir():
                total_size += get_folder_size(entry.path)
    return total_size
