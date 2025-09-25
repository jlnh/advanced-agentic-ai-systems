"""
Researcher Agent - Specialized for information gathering and research tasks.
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain import hub
from config import llm


def create_researcher_agent() -> AgentExecutor:
    """
    Creates a specialized research agent for information gathering.
    Optimized for accuracy and source verification.
    """

    # Specialized prompt that reinforces the agent's role
    researcher_prompt = hub.pull("hwchase17/react").partial(
        system_message="""You are a research specialist with expertise in:
        - Finding accurate, current information from reliable sources
        - Verifying facts and cross-referencing multiple sources
        - Distinguishing between facts and opinions
        - Properly citing sources for transparency

        Your approach:
        1. Start with broad searches, then narrow down
        2. Prioritize authoritative sources (official sites, academic papers)
        3. Always mention source credibility
        4. If information conflicts, note the discrepancy

        You do NOT analyze or interpret data - only gather it."""
    )

    # Curated toolset for research tasks
    research_tools = [
        DuckDuckGoSearchRun(
            name="web_search",
            description="Search the web for current information"
        ),
        Tool(
            name="news_search",
            func=lambda q: search_recent_news(q),  # Custom implementation
            description="Search specifically for recent news articles"
        ),
    ]

    # Create the agent with focused configuration
    agent = create_react_agent(
        llm=llm,
        tools=research_tools,
        prompt=researcher_prompt
    )

    # Wrap in executor with safety limits
    return AgentExecutor(
        agent=agent,
        tools=research_tools,
        verbose=True,  # Enable for debugging
        max_iterations=5,  # Prevent infinite loops
        handle_parsing_errors=True  # Graceful error handling
    )


def search_recent_news(query: str) -> str:
    """Custom news search implementation"""
    # In production, integrate with NewsAPI or similar
    return f"Latest news about {query}: [simulated results]"