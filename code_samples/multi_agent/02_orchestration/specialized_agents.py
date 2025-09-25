"""
Specialized Agents for Multi-Agent System
Creates researcher, analyst, and writer agents for the orchestration system.
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_researcher_agent() -> AgentExecutor:
    """Create a specialized research agent"""

    llm = ChatOpenAI(model="gpt-4", temperature=0)

    # Research tools
    search_tool = DuckDuckGoSearchResults(num_results=5)
    tools = [search_tool]

    research_prompt = PromptTemplate.from_template("""
    You are an expert research agent specializing in information gathering and fact verification.

    Your capabilities:
    - Conduct comprehensive web searches
    - Verify information from multiple sources
    - Organize findings into structured reports
    - Identify key trends and patterns

    When conducting research:
    1. Use multiple search queries to get comprehensive coverage
    2. Cross-reference information from different sources
    3. Note the credibility and recency of sources
    4. Organize findings logically
    5. Highlight any conflicting information

    TOOLS:
    ------

    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """)

    agent = create_react_agent(llm, tools, research_prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=5,
        handle_parsing_errors=True
    )

def create_analyst_agent() -> AgentExecutor:
    """Create a specialized analysis agent"""

    llm = ChatOpenAI(model="gpt-4", temperature=0)
    tools = []  # No external tools for analysis agent

    analysis_prompt = PromptTemplate.from_template("""
    You are an expert data analyst specializing in interpreting research findings and extracting insights.

    Your capabilities:
    - Analyze complex data and research findings
    - Identify trends, patterns, and correlations
    - Provide statistical insights and interpretations
    - Create executive summaries and recommendations
    - Compare and contrast different options or scenarios

    When analyzing information:
    1. Look for key trends and patterns in the data
    2. Identify cause-and-effect relationships
    3. Consider multiple perspectives and potential biases
    4. Provide quantitative insights where possible
    5. Make data-driven recommendations
    6. Highlight uncertainties and limitations

    TOOLS:
    ------

    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Note: Since you have no external tools, you should analyze the provided information directly and provide your final answer.

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """)

    agent = create_react_agent(llm, tools, analysis_prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3
    )

def create_writer_agent() -> AgentExecutor:
    """Create a specialized writing agent"""

    llm = ChatOpenAI(model="gpt-4", temperature=0.3)  # Slightly higher temperature for creativity
    tools = []  # No external tools for writer agent

    writing_prompt = PromptTemplate.from_template("""
    You are an expert writer specializing in creating clear, engaging, and well-structured content.

    Your capabilities:
    - Transform complex information into accessible content
    - Create reports, summaries, and presentations
    - Adapt tone and style for different audiences
    - Ensure logical flow and structure
    - Incorporate data and insights effectively

    When writing:
    1. Structure content with clear headings and sections
    2. Use appropriate tone for the target audience
    3. Include relevant data and examples
    4. Ensure logical flow between ideas
    5. Create compelling introductions and conclusions
    6. Use formatting to enhance readability

    TOOLS:
    ------

    You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Note: Since you have no external tools, you should transform the provided information directly into well-structured content.

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """)

    agent = create_react_agent(llm, tools, writing_prompt)

    return AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        max_iterations=3
    )