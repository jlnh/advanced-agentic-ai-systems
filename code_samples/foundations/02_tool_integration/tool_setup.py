"""
Tool Setup Module - Configure all tools for the multi-tool research agent
"""

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import Tool
from langchain_community.tools import WriteFileTool, ReadFileTool, ListDirectoryTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import tool
import os

def setup_search_tools():
    """Configure web search tools"""
    # Primary web search tool
    search_tool = DuckDuckGoSearchRun(
        name="web_search",
        description="Search the internet for current information. Use for recent news, trends, or factual queries."
    )

    # Wikipedia for reliable reference information
    wikipedia = WikipediaQueryRun(
        api_wrapper=WikipediaAPIWrapper(
            top_k_results=3,
            doc_content_chars_max=1000
        ),
        name="wikipedia_search",
        description="Search Wikipedia for background information on topics, people, or concepts."
    )

    print("🔍 Search tools configured")
    return search_tool, wikipedia

def save_file_custom(input_str: str) -> str:
    """Save text content to a file in the workspace.

    Input should be in format: file_path='filename.ext' text='content to save'
    """
    workspace_dir = "./agent_workspace"
    os.makedirs(workspace_dir, exist_ok=True)

    try:
        # Parse the input string to extract file_path and text
        import re

        # Extract file_path
        file_path_match = re.search(r"file_path=['\"]([^'\"]+)['\"]", input_str)
        if not file_path_match:
            return "Error: file_path parameter required in format file_path='filename.ext'"

        file_path = file_path_match.group(1)

        # Extract text
        text_match = re.search(r"text=['\"](.+?)['\"](?:\s|$)", input_str, re.DOTALL)
        if not text_match:
            return "Error: text parameter required in format text='content to save'"

        text = text_match.group(1)

        full_path = os.path.join(workspace_dir, file_path)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return f"Successfully saved content to {file_path}"
    except Exception as e:
        return f"Error saving file: {str(e)}"

# Create tool wrapper
save_file_tool = Tool(
    name="save_file",
    description="Save text content to a file. Format: file_path='filename.ext' text='content to save'",
    func=save_file_custom
)

def setup_file_tools():
    """Configure file management tools"""
    # Ensure workspace directory exists
    workspace_dir = "./agent_workspace"
    os.makedirs(workspace_dir, exist_ok=True)

    read_tool = ReadFileTool(
        root_dir=workspace_dir,
        name="read_file",
        description="Read content from previously saved files."
    )

    list_tool = ListDirectoryTool(
        root_dir=workspace_dir,
        name="list_files",
        description="List all files in the workspace directory."
    )

    print("📁 File tools configured")
    return save_file_tool, read_tool, list_tool