# src/agentic_ai/core/tools/registry.py
from typing import Dict, List, Any
from langchain.tools import Tool, DuckDuckGoSearchTool
from langchain.tools.python.tool import PythonREPLTool
from langchain.tools.file_management import WriteFileTool, ReadFileTool
import os

class ToolRegistry:
    """Central registry for all agent tools"""
    
    def __init__(self):
        self._tools = {}
        self._initialize_default_tools()
    
    def _initialize_default_tools(self):
        """Initialize commonly used tools"""
        
        # Ensure workspace directory exists
        workspace_dir = "./workspace"
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Web search
        self.register_tool(
            "web_search",
            DuckDuckGoSearchTool(
                name="web_search",
                description="Search the internet for current information and recent developments"
            )
        )
        
        # Python execution
        self.register_tool(
            "python_repl",
            PythonREPLTool(
                description="Execute Python code for calculations, data analysis, and processing"
            )
        )
        
        # File operations
        self.register_tool(
            "write_file",
            WriteFileTool(
                root_dir=workspace_dir,
                description="Write content to files in the workspace directory"
            )
        )
        
        self.register_tool(
            "read_file", 
            ReadFileTool(
                root_dir=workspace_dir,
                description="Read content from files in the workspace directory"
            )
        )
    
    def register_tool(self, name: str, tool: Tool):
        """Register a new tool"""
        self._tools[name] = tool
    
    def get_tool(self, name: str) -> Tool:
        """Get tool by name"""
        return self._tools.get(name)
    
    def get_tools_by_category(self, category: str) -> List[Tool]:
        """Get tools for specific agent types"""
        tool_categories = {
            "research": ["web_search"],
            "analysis": ["python_repl", "web_search"], 
            "writing": ["write_file", "read_file"],
            "general": list(self._tools.keys())
        }
        
        tool_names = tool_categories.get(category, [])
        return [self._tools[name] for name in tool_names if name in self._tools]
    
    def list_tools(self) -> Dict[str, str]:
        """List all available tools"""
        return {name: tool.description for name, tool in self._tools.items()}

# Global tool registry instance
tool_registry = ToolRegistry()