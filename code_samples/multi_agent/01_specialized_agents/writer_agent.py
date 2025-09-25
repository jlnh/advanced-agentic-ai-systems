"""
Writer Agent - Specialized for content creation and formatting.
"""

import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.tools.file_management import WriteFileTool
from langchain import hub
from config import llm


def create_writer_agent() -> AgentExecutor:
    """
    Creates a specialized writer agent for content generation.
    Optimized for clarity, structure, and audience adaptation.
    """

    writer_prompt = hub.pull("hwchase17/react").partial(
        system_message="""You are a professional content writer with expertise in:
        - Creating clear, engaging, and well-structured content
        - Adapting tone and style for different audiences
        - Organizing information logically with proper hierarchy
        - Ensuring consistency in formatting and voice

        Your approach:
        1. Identify the target audience and purpose
        2. Create a clear structure (intro, body, conclusion)
        3. Use appropriate formatting (headings, bullets, etc.)
        4. Review for clarity and flow

        You do NOT research or analyze - only write and format."""
    )

    # Create outputs directory if it doesn't exist
    output_dir = "./outputs"
    os.makedirs(output_dir, exist_ok=True)

    writing_tools = [
        WriteFileTool(
            root_dir=output_dir,  # Controlled output directory
            description="Save formatted content to files"
        ),
        Tool(
            name="format_markdown",
            func=lambda text: format_as_markdown(text),
            description="Format text as clean Markdown"
        ),
        Tool(
            name="create_summary",
            func=lambda text: create_executive_summary(text),
            description="Create concise executive summary"
        ),
    ]

    agent = create_react_agent(
        llm=llm,
        tools=writing_tools,
        prompt=writer_prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=writing_tools,
        verbose=True,
        max_iterations=3  # Writing typically needs fewer iterations
    )


def format_as_markdown(text: str) -> str:
    """Convert text to well-formatted Markdown"""
    # Add proper headers, lists, emphasis
    return f"# Summary\n\n{text}"


def create_executive_summary(text: str, max_length: int = 500) -> str:
    """Generate concise executive summary"""
    # In production, use LLM for summarization
    return text[:max_length] + "..."