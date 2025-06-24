import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_wd = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file.startswith(abs_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(abs_file):
        return f'Error: File "{file_path}" not found.'

    if os.path.splitext(file_path)[1] != '.py':
        return f'Error: "{file_path}" is not a Python file.'

    timeout = 30

    try:
        completed_proc = subprocess.run(
            ["python3", file_path],
            capture_output = True,
            timeout = timeout,
            cwd = os.path.dirname(abs_file)
        )

        output = f'STDOUT: {completed_proc.stdout}\r\nSTDERR: {completed_proc.stderr}\r\n'

        returncode = ''
        if completed_proc.returncode!=0 :
             returncode = f'Process exited with code {completed_proc.returncode}\r\n'

        if len(completed_proc.stdout) == 0 and len(completed_proc.stderr) == 0:
            output = 'No output produced.'

        return output+returncode

    except Exception as e:
        return f"Error: executing Python file: {e}"

