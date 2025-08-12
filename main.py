import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import *



def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt #system_instruction = types.Part(text = system_prompt)
        )
    )
    if verbose:
        print(f"User prompt: {user_prompt}\\n")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if response.function_calls:
        print("Response:")
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})")
    else:
        print("Response:")
        print(response.text)





def main():
    
    

    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    user_prompt = " ".join(args)
    verbose = "--verbose" in sys.argv

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    #verify correct program usage
    if user_prompt == "":
        print('ERROR: uv run main.py "Enter your prompt here" ')
        sys.exit(1)


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    generate_content(client,messages,verbose, user_prompt)
    


if __name__ == "__main__":
    main()