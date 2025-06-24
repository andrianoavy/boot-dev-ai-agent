import os


def write_file(working_directory, file_path, content):
    abs_wd = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(abs_wd):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    abs_file_dir = os.path.dirname(abs_file)
    if not os.path.exists(abs_file_dir):
        os.makedirs(abs_file_dir)

    with open(abs_file, "w") as f:
        f.write(content)

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
