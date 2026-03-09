from google.adk.agents import Agent
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file import write_file
from functions.run_python_file import run_python_file

from prompts import system_prompt

import os

def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

OLLAMA_API_BASE = os.getenv("OLLAMA_API_BASE", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

print("---" * 30)
print(f"Using Ollama API Base: {OLLAMA_API_BASE}")
print(f"Using Ollama Model: {OLLAMA_MODEL}")
print("---" * 30)

# Ensure ADK treats this as a chat model and knows where Ollama lives
ollama_llm = LiteLlm(
    model=f"ollama_chat/{OLLAMA_MODEL}",
    api_base=OLLAMA_API_BASE,
)

root_agent = Agent(
    #model='gemini-2.5-flash-lite-preview-09-2025',
    model = ollama_llm,
    name='my_adk_agent',
    description='You are a claude code clone',
    instruction=system_prompt,
    tools=[get_file_content, get_files_info, write_file, run_python_file],
)
