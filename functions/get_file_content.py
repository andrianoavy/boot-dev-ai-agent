import os

MAX_CHARS = 10000

def get_file_content(working_directory, file_path):
    abs_wd = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory,file_path))
    
    if not abs_file.startswith(abs_wd): 
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file): 
        return f'Error: File not found or is not a regular file: "{file_path}"'

    try:
        with open(abs_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            return file_content_string + f'...File "{file_path}" truncated at {MAX_CHARS} characters'
    except Exception as e:
        return f'Error: {e.args}'
