import os
import argparse
from google import genai
from google.genai import types
from dotenv import load_dotenv

from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

MAX_ITERATIONS = 20

def main():
    
    if not api_key:
        raise Exception("GEMINI_API_KEY not found in environment variables.")

    if not gemini_model:
        raise Exception("GEMINI_MODEL not found in environment variables.")
  
  

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    args = parser.parse_args()
    user_prompt = args.user_prompt
    verbose = args.verbose
    
    if verbose:
        print("Hello from claude-code-clone!")
        print("API Key loaded successfully.")
        print(f"Using Gemini model: {gemini_model}")    
    
    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    client = genai.Client(api_key=api_key)
    ##client.models.list()
    
    iteration = 0
    while iteration < MAX_ITERATIONS:
        try:
            response = client.models.generate_content(
                model=gemini_model,
                contents=messages,
                config=types.GenerateContentConfig(system_instruction=system_prompt,
                                                    tools=[available_functions])                                      
            )
            
            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Response from Gemini API: {response}")
                print("=" * 100)
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            
            # determine if there are function calls in the response
            if not response.function_calls and response:
                # print the response and exit the loop
                print(f"Final Response:\n {response.text}")
                break  # exit loop if no function calls
            
            if verbose:
                for candidate in response.candidates:
                    print(f"Candidate content: {candidate.content}")
            
            function_call_response = []
            print("-" * 100)
            if response.function_calls:
                for function_call in response.function_calls:                
                    function_response_content = call_function(function_call, verbose=verbose)
                    if function_response_content.parts[0].function_response.response:
                        function_call_response.append(function_response_content.parts[0])
                        function_response_text = function_response_content.parts[0].function_response.response['result']
                        if verbose:
                            print(f"-> {function_response_text}")
                        messages.append(types.Content(role="user", parts=[types.Part(text=function_response_text)]))
                    else:
                        raise Exception(f"Function {function_call.name}({function_call.args}) call failed.")
            else:
                if verbose:
                    print(f"Response from Gemini API: {response.text}")
                
            iteration += 1
         
            print(f"Iteration: {iteration}")
            #print("=" * 100)
        except Exception as e:
            e.print_stack()
            print(f"An error occurred: {e}")
            break
        

if __name__ == "__main__":
    main()
