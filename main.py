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

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages,
)

prompt_tokens = response.usage_metadata.prompt_token_count
response_tokens = response.usage_metadata.candidates_token_count

if verbose:
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {prompt_tokens}")
    print(f"Response tokens: {response_tokens}")
