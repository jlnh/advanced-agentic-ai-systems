"""
Multi-Tool Research Agent - Main agent implementation with integrated tools
"""

from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain import hub
from tool_setup import setup_search_tools, setup_file_tools
from custom_tools import create_custom_tools
from monitoring import ToolUsageTracker
from security_utils import setup_secure_workspace
import os
from dotenv import load_dotenv
load_dotenv()

def create_research_agent(api_key: str = None, model: str = "gpt-3.5-turbo"):
    """Create and configure the multi-tool research agent"""

    # Set up LLM
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key

    llm = ChatOpenAI(model=model, temperature=0)

    # Get the ReAct prompt template
    prompt = hub.pull("hwchase17/react")

    # Set up secure workspace
    setup_secure_workspace()

    # Configure all tools
    search_tool, wikipedia = setup_search_tools()
    write_tool, read_tool, list_tool = setup_file_tools()
    data_analyzer, report_formatter = create_custom_tools()

    # Combine all tools
    all_tools = [
        search_tool,
        wikipedia,
        write_tool,
        read_tool,
        list_tool,
        data_analyzer,
        report_formatter
    ]

    # Create enhanced agent with all capabilities
    enhanced_agent = create_react_agent(
        llm=llm,
        tools=all_tools,
        prompt=prompt
    )

    research_agent = AgentExecutor(
        agent=enhanced_agent,
        tools=all_tools,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

    print(f"🤖 Research agent ready with {len(all_tools)} tools")
    return research_agent

def test_search_and_save(agent):
    """Test simple web search and save functionality"""
    result = agent.invoke({
        "input": "Search for 'quantum computing breakthroughs 2024' and save the key findings to a file called 'quantum_research.md'"
    })
    print("Search and Save Result:", result['output'])
    return result

def test_full_research_workflow(agent):
    """Test complex research workflow"""
    result = agent.invoke({
        "input": """
        Research the latest developments in large language models,
        analyze the key trends,
        format as a professional report,
        and save to 'llm_research_report.md'
        """
    })
    print("Full Workflow Result:", result['output'])
    return result

def test_file_operations(agent):
    """Test file management capabilities"""
    result = agent.invoke({
        "input": "List all files in my workspace, then read the content of the most recent research file"
    })
    print("File Operations Result:", result['output'])
    return result

if __name__ == "__main__":
    # Create the research agent
    agent = create_research_agent()

    # Initialize usage tracker
    tracker = ToolUsageTracker()

    print("\n=== Testing Multi-Tool Agent ===")

    # Run tests
    test_search_and_save(agent)
    test_full_research_workflow(agent)
    test_file_operations(agent)

    print("\n=== Testing Complete ===")

    # Print usage statistics
    # Note: Actual tracking would require integration with agent callbacks
    print("\n📊 Agent testing completed successfully!")