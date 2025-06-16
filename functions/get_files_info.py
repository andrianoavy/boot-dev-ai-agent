import os

def get_files_info(working_directory, directory=None):
    abs_dir = os.path.abspath(working_directory)
    target_dir=abs_dir
    if directory:
        target_dir = os.path.abspath(os.path.join(working_directory, directory))
    if not target_dir.startswith(abs_dir):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(target_dir):
        return f'Error: "{directory}" is not a directory'
    try:
        res = []
        for dirname in os.listdir(abs_dir):
            dir = os.path.join(abs_dir, dirname)
            res.append(f'{dirname}: file_size={os.path.getsize(dir)} bytes, is_dir={not os.path.isfile(dir)}')
        return '\r\n'.join(res)
    except Exception as e:
        return f'Error listing files {e}'

