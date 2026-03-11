import os
import argparse

from typing import List

from google import genai
from google.genai import Client
from google.genai import types
from dotenv import load_dotenv

from rich.console import Console
from rich.panel import Panel

from prompts import system_prompt
from functions.call_function import available_functions
from functions.call_function import call_function


MAX_ITERATIONS = 20

def agentic_loop(client: Client, model: str, user_prompt: str, messages:List[str], verbose: bool):
    iteration = 0
    client_config = types.GenerateContentConfig(system_instruction=system_prompt,
                                                tools=[available_functions])
    while iteration < MAX_ITERATIONS:
        try:
            response = client.models.generate_content(
                model=model,
                contents=messages,
                config=client_config
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
                return f"Final Response:\n {response.text}"                
                    
            # looping through response.candidaates
            if response.candidates:
                if verbose:
                    print ("### response.candidates")
                for i, candidate in enumerate(response.candidates): 
                    if verbose:
                        print(f"Response candidate content[{i}] ({candidate.content.role}): {candidate.content.parts[0].text} - {candidate.content}")
                    messages.append(candidate.content)
            
            function_call_response = []
            print("-" * 100)
            if response.function_calls:
                for i, function_call in enumerate(response.function_calls): 
                    if verbose:
                        print(f"function_call content[{i}] {function_call}")
                    function_response_content = call_function(function_call, verbose=verbose)
                    if verbose:
                        print(f"call_function response[{i}]: {function_response_content}")
                    messages.append(function_response_content)                    
            else:
                print(f"Final response: {response.text}")
                return
                
            iteration += 1
            if verbose:
                print(f"------  Iteration: {iteration}\n")
            
        except Exception as e:
            e.print_stack()
            return f"An error occurred: {e}"
            

def print_banner():
    console = Console()
    # ASCII Art string
    banner_text = """
       ________                __         ______            __      ______                      
      / ____/ /___ ___  ______/ /__      / ____/___  ____  / /__   / ____/___  ____/ /__        
     / /   / / __ `/ / / / __  / _ \    / /   / __ \/ __ \/ / _ \ / /   / __ \/ __  / _ \       
    / /___/ / /_/ / /_/ / /_/ /  __/   / /___/ /_/ / /_/ / /  __// /___/ /_/ / /_/ /  __/       
    \____/_/\__,_/\__,_/\__,_/\___/    \____/\____/\____/_/\___/ \____/\____/\__,_/\___/        
    """

    # Rich makes it easy to style the whole block with a gradient-like border
    console.print(banner_text, style="bold color(27)") # Deep Blue
    console.print(Panel("[bold magenta]Claude Code Clone[/bold magenta] v1.0.0", expand=False))

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    if not api_key:
        raise Exception("GEMINI_API_KEY not found in environment variables.")

    if not gemini_model:
        raise Exception("GEMINI_MODEL not found in environment variables.")

    print_banner()

    print("---" * 30)
    print(f"Starting agent with model: {gemini_model}")
    print("---" * 30)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    
    args = parser.parse_args()
    verbose = args.verbose
    
    if verbose:
        print("Hello from claude-code-clone!")
        print("API Key loaded successfully.")
        print(f"Configured model: {gemini_model}")    
    
    # instantia gemini client
    client = genai.Client(api_key=api_key)
    if verbose:
        print(f"client model list: {type(client.models.list())}")
        
    messages = []
    while True:
        user_prompt = input("[user]: ")
        
        user_prompt_lowercase = user_prompt.lower()
        if user_prompt_lowercase == "/exit" or user_prompt_lowercase == "/bye":
            print("[agent] Goodbye!")
            break
        elif user_prompt_lowercase == "/clear":
            messages = []
            continue
        elif user_prompt_lowercase == "/help":
            print("[agent] no help for")
            print("\n")
            continue
            
        # perform action
        print(f"action: {user_prompt}")
        messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))        
    
        # go into agentic loop
        agent_response = agentic_loop(client, gemini_model, user_prompt, messages, verbose)        
        
        # print agent out
        print(f"[agent] {agent_response}")
        print("-" * 40)
            
        
if __name__ == "__main__":
    main()
