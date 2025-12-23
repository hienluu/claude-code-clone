## Claude Code Clone AI agent
This is a simple AI coding agent that uses Gemini as the LLM and it has access to 4 tools, which are defined in the function directory.  


### Getting started
* make a copy of .env.sample and name if .env
* populate your GEMINI_API_KEY
* Warning: as you try to test this out, you might run in the Gemini rate limiting, unless you've set up a paid tier with your credit card.

### Example prompts
* uv run main.py "tell me about the calculator's capabilities"
* uv run main.py "how does the calculator work?"


### Resources
* This is based on the course [AI Agents on boot.dev](https://www.boot.dev/courses/build-ai-agent-python)
* Youtube video: [Guide to Agentic AI – Build a Python Coding Agent with Gemini](https://www.youtube.com/watch?v=YtHdaXuOAks)