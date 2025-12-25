import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt

from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")

    generate_content(client, messages, args.verbose)


def generate_content(client, messages, verbose):
    max_iterations = 20

    for iteration in range(max_iterations):
        if verbose:
            print(f"\n--- Iteration {iteration + 1} ---")

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                ),
            )

            if not response.usage_metadata:
                raise RuntimeError("Gemini API response appears to be malformed")

            if verbose:
                print("Prompt tokens:", response.usage_metadata.prompt_token_count)
                print(
                    "Response tokens:", response.usage_metadata.candidates_token_count
                )

            # Add all candidates' content to messages
            for candidate in response.candidates:
                messages.append(candidate.content)

            # Check if the model is finished (no function calls and has text)
            has_function_calls = False
            for candidate in response.candidates:
                for part in candidate.content.parts:
                    if hasattr(part, "function_call") and part.function_call:
                        has_function_calls = True
                        break
                if has_function_calls:
                    break

            # If finished (no function calls and has text response)
            if not has_function_calls and response.text:
                print("Response:")
                print(response.text)
                break

            # If there are function calls, execute them
            if has_function_calls:
                function_responses = []
                for candidate in response.candidates:
                    for part in candidate.content.parts:
                        if hasattr(part, "function_call") and part.function_call:
                            result = call_function(part.function_call, verbose)
                            if (
                                not result.parts
                                or not result.parts[0].function_response
                                or not result.parts[0].function_response.response
                            ):
                                raise RuntimeError(
                                    f"Empty function response for {part.function_call.name}"
                                )
                            if verbose:
                                print(
                                    f"-> {result.parts[0].function_response.response}"
                                )
                            function_responses.append(result.parts[0])

                # Add function responses to messages as user role
                if function_responses:
                    messages.append(
                        types.Content(role="user", parts=function_responses)
                    )

            # Check if we've reached max iterations
            if iteration == max_iterations - 1:
                print("Response:")
                print("Maximum iterations reached.")
                break

        except Exception as e:
            print(f"Error during iteration {iteration + 1}: {e}")
            break


main()
