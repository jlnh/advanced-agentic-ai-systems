# src/agentic_ai/core/agents/specialized.py
from typing import List
from .react_agent import ReActAgent
from ..tools.registry import tool_registry

class ResearchAgent(ReActAgent):
    """Specialized agent for research and information gathering"""
    
    def __init__(self):
        tools = tool_registry.get_tools_by_category("research")
        super().__init__("researcher", tools, model="gpt-3.5-turbo")
    
    def get_capabilities(self) -> List[str]:
        return [
            "web_search",
            "fact_verification", 
            "source_citation",
            "information_synthesis"
        ]

class AnalystAgent(ReActAgent):
    """Specialized agent for data analysis and computation"""
    
    def __init__(self):
        tools = tool_registry.get_tools_by_category("analysis")
        super().__init__("analyst", tools, model="gpt-3.5-turbo")
    
    def get_capabilities(self) -> List[str]:
        return [
            "data_analysis",
            "statistical_computation",
            "pattern_recognition",
            "quantitative_reasoning"
        ]

class WriterAgent(ReActAgent):
    """Specialized agent for content creation and formatting"""
    
    def __init__(self):
        tools = tool_registry.get_tools_by_category("writing")
        super().__init__("writer", tools, model="gpt-4")  # Better model for writing
    
    def get_capabilities(self) -> List[str]:
        return [
            "content_creation",
            "document_formatting",
            "style_adaptation",
            "editing_refinement"
        ]