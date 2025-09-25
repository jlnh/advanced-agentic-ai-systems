"""
Analyst Agent - Specialized for data processing, analysis, and visualization.
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_experimental.tools import PythonREPLTool
from langchain import hub
from typing import Dict
from config import llm


def create_analyst_agent() -> AgentExecutor:
    """
    Creates a specialized analyst agent for data processing.
    Optimized for computation, pattern finding, and visualization.
    """

    analyst_prompt = hub.pull("hwchase17/react").partial(
        system_message="""You are a data analyst with expertise in:
        - Statistical analysis and pattern recognition
        - Data visualization and chart creation
        - Quantitative comparisons and calculations
        - Trend identification and insights extraction

        Your approach:
        1. Clean and validate data before analysis
        2. Use appropriate statistical methods
        3. Create clear visualizations when helpful
        4. Provide confidence levels for your findings

        You do NOT gather new data - only analyze what's provided."""
    )

    # Python REPL with pre-configured libraries
    python_tool = PythonREPLTool(
        description="""Use for data analysis. Available libraries:
        - pandas for data manipulation
        - numpy for numerical operations
        - matplotlib/plotly for visualization
        - scipy for statistics"""
    )

    # Custom analysis tool with sandboxed environment
    analysis_tools = [
        python_tool,
        Tool(
            name="calculate_statistics",
            func=lambda data: calculate_stats(data),
            description="Calculate mean, median, std dev, and percentiles"
        ),
    ]

    agent = create_react_agent(
        llm=llm,
        tools=analysis_tools,
        prompt=analyst_prompt
    )

    return AgentExecutor(
        agent=agent,
        tools=analysis_tools,
        verbose=True,
        max_execution_time=30,  # Timeout for long computations
        max_iterations=10  # More iterations for complex analysis
    )


def calculate_stats(data: str) -> Dict[str, float]:
    """Helper for quick statistical calculations"""
    # Parse and compute statistics
    # This is a simplified example
    return {
        "mean": 0.0,
        "median": 0.0,
        "std_dev": 0.0
    }