import sys
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

if len(sys.argv) < 2:
    print("Please give me a prompt!")
    os.exit(1)

user_prompt = sys.argv[1]
verbose = False

if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    verbose = True

api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

schema_get_file_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the content of the specified file, within a limit of 10000 characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to read the content of, relative to the working directory. If not provided, return an error.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute the specified python file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to execute , relative to the working directory. If not provided, return an error.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the specified content in the specified file, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file": types.Schema(
                type=types.Type.STRING,
                description="The file to write in, relative to the working directory. If not provided. Return an error.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write in the file.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[
        schema_get_file_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file
    ]
)

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

"""
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
    config=types.GenerateContentConfig(system_instruction=system_prompt, tools=[available_functions])
)

print(f"Answer: {response.text}")

for fn in response.function_calls: 
    print(f"Calling function: {fn.name}({fn.args})")

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
