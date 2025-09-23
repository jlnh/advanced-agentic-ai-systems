"""
Debugging Utilities for ReAct Agent

This module contains debugging tools and utilities to help understand
the internal workings of the ReAct agent execution process.
"""

from langchain.agents import AgentExecutor
from langchain.tools import Tool, PythonREPLTool
from langchain.prompts import PromptTemplate


class DebuggingAgentExecutor(AgentExecutor):
    """
    Enhanced AgentExecutor that provides detailed debugging information
    about the agent's thought process and execution flow.

    Note: This is a conceptual implementation. The actual LangChain AgentExecutor
    has a more complex internal structure. This serves as an educational example
    of how the ReAct loop works conceptually.
    """

    def _call(self, inputs):
        """
        Execute the agent with detailed debugging output.

        This method shows the conceptual flow of:
        Thought → Action → Observation → repeat until done
        """
        print(f"🤖 Agent received: {inputs['input']}")

        # Note: This is a simplified version for educational purposes
        # The actual implementation would interact with the agent's internal methods
        print("\n💡 This is a conceptual debugging implementation.")
        print("The actual AgentExecutor has a more complex internal structure.")
        print("For real debugging, use verbose=True in AgentExecutor.")

        # Call the parent implementation
        return super()._call(inputs)


def create_debugging_agent():
    """Create an agent with enhanced debugging capabilities."""
    from react_agent import create_basic_agent

    # Create the basic agent
    agent_executor = create_basic_agent()

    # For actual debugging, we recommend using verbose=True
    # which is already set in the basic agent creation
    print("🔍 Debugging enabled via verbose=True in AgentExecutor")
    print("This will show the actual thought process and tool usage.")

    return agent_executor


def create_custom_tool_with_description():
    """
    Example of creating a custom tool with clear description
    to help the agent choose the right tool.
    """
    calculator = Tool(
        name="Calculator",
        func=lambda x: str(eval(x)),  # Simplified - use PythonREPLTool in practice
        description="Use this for ANY mathematical calculations. Input should be a Python expression."
    )
    return calculator


def create_custom_prompt():
    """
    Create a custom ReAct prompt template for better performance.
    """
    custom_prompt = PromptTemplate.from_template("""
You are a helpful assistant that can use tools to solve problems.

IMPORTANT: Always show your reasoning step by step.

Available tools: {tools}

Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}
""")
    return custom_prompt


def debug_agent_execution(agent_executor, query, show_internals=True):
    """
    Execute agent with comprehensive debugging information.
    """
    print(f"🚀 Starting agent execution for: '{query}'")
    print("=" * 60)

    if show_internals:
        print("🔧 Agent Configuration:")
        print(f"  - Model: {agent_executor.agent.llm_chain.llm.model_name}")
        print(f"  - Tools: {[tool.name for tool in agent_executor.tools]}")
        print(f"  - Max iterations: {agent_executor.max_iterations}")
        print(f"  - Verbose: {agent_executor.verbose}")
        print()

    try:
        result = agent_executor.invoke({"input": query})
        print("✅ Execution completed successfully!")
        return result
    except Exception as e:
        print(f"❌ Execution failed: {e}")
        print("\n🔍 Debugging tips:")
        print("1. Check your OpenAI API key")
        print("2. Verify internet connection for hub.pull()")
        print("3. Try a simpler query first")
        print("4. Check tool descriptions and inputs")
        return {"output": f"Error: {e}"}


if __name__ == "__main__":
    print("ReAct Agent Debugging Utilities")
    print("This module provides tools for debugging agent execution.")
    print("\nTo use these utilities:")
    print("1. Import the functions you need")
    print("2. Create an agent using create_debugging_agent()")
    print("3. Use debug_agent_execution() for detailed output")

    # Example usage
    print("\nExample usage:")
    print("from debug_utils import create_debugging_agent, debug_agent_execution")
    print("agent = create_debugging_agent()")
    print("debug_agent_execution(agent, 'What is 25% of 1380?')")