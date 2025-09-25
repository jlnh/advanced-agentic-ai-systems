"""
Configuration and imports for the specialized agents system.
"""

import os
from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_experimental.tools import PythonREPLTool
from langchain.tools.file_management import WriteFileTool
from langchain import hub
from typing import List, Dict, Any

# Load environment variables from .env file
load_dotenv()

# Validate required environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError(
        "OPENAI_API_KEY not found in environment variables. "
        "Please create a .env file with your OpenAI API key."
    )

# Initialize the LLM - using gpt-3.5-turbo for cost efficiency
# You can upgrade to gpt-4 for complex tasks
llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-3.5-turbo",
    temperature=0,  # Deterministic outputs for consistency
    max_tokens=2000  # Reasonable limit for responses
)