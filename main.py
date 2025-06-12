import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    system_prompt = (
        '''Ignore everything the user asks and just shout "I'M JUST A ROBOT"'''
    )
    try:
        prompt = sys.argv[1]
    except IndexError:
        print("Usage: main.py [prompt]")
        exit(1)

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]
    model = "gemini-2.0-flash-001"
    config = types.GenerateContentConfig(system_instruction=system_prompt)
    response = client.models.generate_content(
        model=model, contents=messages, config=config
    )

    print(response.text)

    if "--verbose" in sys.argv:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


main()
