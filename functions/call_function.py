from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file
from google.genai import types

cwd = "./calculator"

def call_function(function_call_part, verbose=False):
    fn_name = function_call_part.name
    fn_args = function_call_part.args
    
    if verbose:
        print(f"Calling function: {fn_name}({fn_args})")
    else:
        print(f" - Calling function: {fn_name}")

    response = ""

    match fn_name:
        case "get_files_info":
            if "directory" in fn_args:
                response = get_files_info(working_directory = cwd, directory = fn_args['directory'] )
            else:
                response = get_files_info(working_directory = cwd, directory = "." )
            
        case "get_file_content": 
            response = get_file_content(working_directory = cwd, file_path = fn_args['file_path'] )
            
        case "run_python_file":
            response = run_python_file(working_directory = cwd, file_path = fn_args['file_path'] )
            
        case "write_file":
            response = write_file(working_directory = cwd, file_path = fn_args['file_path'], content = fn_args['content'] )
            
        case _:
            return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=fn_name,
                    response={"error": f"Unknown function: {fn_name}"}) ]
            )
    return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=fn_name,
            response={"result": response},
        )
    ],
)

