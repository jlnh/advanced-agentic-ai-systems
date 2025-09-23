"""
Tool Setup Module - Configure all tools for the multi-tool research agent
"""

from langchain.tools import DuckDuckGoSearchTool, Tool
from langchain.tools.file_management import WriteFileTool, ReadFileTool, ListDirectoryTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
import os

def setup_search_tools():
    """Configure web search tools"""
    # Primary web search tool
    search_tool = DuckDuckGoSearchTool(
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

def setup_file_tools():
    """Configure file management tools"""
    # Ensure workspace directory exists
    workspace_dir = "./agent_workspace"
    os.makedirs(workspace_dir, exist_ok=True)

    # File operation tools
    write_tool = WriteFileTool(
        root_dir=workspace_dir,
        name="save_file",
        description="Save text content to a file. Use for storing reports, analysis, or research findings."
    )

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
    return write_tool, read_tool, list_tool