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

def agentic_loop(client: Client, model: str, messages:List[str], verbose: bool):
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
    from banner import print_banner
    print_banner()

def print_messages(messages: List[types.Content]):
    if not messages:
        print("[agent] No messages in conversation history")
        return
    print("[agent] Conversation history:")
    for i, msg in enumerate(messages, 1):
        role = msg.role

        if role == "user":
            text = (msg.parts[0].text or "(empty)") if msg.parts else "(empty)"
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"  {i}. [USER]: {preview}")

        elif role == "model":
            content_parts = []
            for part in msg.parts:
                if hasattr(part, 'text') and part.text:
                    content_parts.append(part.text)
                elif hasattr(part, 'function_call'):
                    fc = part.function_call
                    func_name = fc.name if hasattr(fc, 'name') else "unknown"
                    args = fc.args if hasattr(fc, 'args') else {}
                    content_parts.append(f"[Function: {func_name}({args})]")

            content = " ".join(content_parts) if content_parts else "(empty)"
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f"  {i}. [MODEL]: {preview}")

        elif role == "tool":
            content_parts = []
            for part in msg.parts:
                if hasattr(part, 'function_response'):
                    fr = part.function_response
                    func_name = fr.name if hasattr(fr, 'name') else "unknown"
                    response_data = fr.response if hasattr(fr, 'response') else {}
                    content_parts.append(f"[Tool Response: {func_name} -> {response_data}]")
                elif hasattr(part, 'text') and part.text:
                    content_parts.append(part.text)

            content = " ".join(content_parts) if content_parts else "(empty)"
            preview = content[:100] + "..." if len(content) > 100 else content
            print(f"  {i}. [TOOL]: {preview}")

        else:
            text = (msg.parts[0].text or "(empty)") if msg.parts else "(empty)"
            preview = text[:100] + "..." if len(text) > 100 else text
            print(f"  {i}. [{role.upper()}]: {preview}")

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
        model_list = client.models.list()
        if hasattr(model_list, "models"):
            model_list = model_list.models
        else:
            model_list = list(model_list)
        print(f"client model list: {model_list}")
        
    messages = []
    while True:
        user_prompt = input("[user]: ")
        
        user_prompt_lowercase = user_prompt.lower()
        if user_prompt_lowercase in ["/exit", "/bye", "/quit"]:
            print("[agent] Goodbye!")
            break
        elif user_prompt_lowercase == "/clear":
            messages = []
            continue
        elif user_prompt_lowercase == "/help":
            print("[agent] /exit or /bye to exit, /clear to clear the conversation, /messages to view conversation history, /help for this message")
            print("\n")
            continue
        elif user_prompt_lowercase == "/messages":
            print_messages(messages)
            print("\n")
            continue
            
        # perform action
        print(f"action: {user_prompt}")
        messages.append(types.Content(role="user", parts=[types.Part(text=user_prompt)]))        
    
        # go into agentic loop
        agent_response = agentic_loop(client, gemini_model, messages, verbose)        
        
        # print agent out
        print(f"[agent] {agent_response}")
        print("-" * 40)
            
        
if __name__ == "__main__":
    main()
