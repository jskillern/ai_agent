import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import *

function_map_dictionary = {
    "get_file_content" : get_file_content,
    "get_files_info":  get_files_info,
    "run_python_file" : run_python_file,
    "write_file" : write_file,
    }

def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
        model=model_name,
        contents=messages,
        config = types.GenerateContentConfig(
            tools = [available_functions],
            system_instruction = system_prompt
        )
    )
    if verbose:
        print(f"User prompt: {user_prompt}\\n")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    if response.function_calls:
        print("Response:")
        function_call_result = call_function(response.function_calls[0], verbose)
        try:
            response_data = function_call_result.parts[0].function_response.response
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        except Exception as e:
            raise Exception("Fatal Error: Unexpected function call result structure.")

    else:
        print("Response:")
        print(response.text)
    return response



def call_function(function_call_part, verbose=False):
    if function_call_part.name not in function_map_dictionary:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    function_call_part.args["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    called_function = function_map_dictionary[function_call_part.name](**function_call_part.args)
    
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": called_function},
            )
        ],
    )



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


    
    if user_prompt == "":
        print('ERROR: uv run main.py "Enter your prompt here" ')
        sys.exit(1)


    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    
    for attempt in range(20):
        response = generate_content(client, messages, verbose, user_prompt)

        for candidate in getattr(response, "candidates", []):
            messages.append(candidate.content)

    # Handle function/tool calls and add tool output message if needed
        if getattr(response, "function_calls", None):
            for function_call in response.function_calls:
                function_result = call_function(response.function_calls[0], verbose)
                messages.append(function_result)

    # Only break and print when 
    # - there are no more function_calls
    # - and response.text is present (so, end of thinking)
        if (not getattr(response, "function_calls", None) 
            and hasattr(response, "text") 
            and response.text):
            print("Final response:")
            print(response.text)
            break


if __name__ == "__main__":
    main()