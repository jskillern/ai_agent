import os
import sys
from google import genai
from google.genai import types
from dotenv import load_dotenv




def generate_content(client, messages, verbose, user_prompt):
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )
    if verbose:
        print(f"User prompt: {user_prompt}\\n")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
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