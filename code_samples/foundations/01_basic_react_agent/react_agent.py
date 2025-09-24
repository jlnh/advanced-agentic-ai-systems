"""
Basic ReAct Agent Implementation

This module contains the core ReAct agent setup from Module 1 Task 1.
The ReAct (Reasoning and Acting) pattern allows an AI agent to think step-by-step
and take actions to solve problems.
"""

import os
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain_experimental.tools import PythonREPLTool
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

def setup_environment():
    """Set up the environment and API key."""
    # You need to set your OpenAI API key in .env file or as an environment variable
    # Either set it as an environment variable or uncomment the line below:
    # os.environ["OPENAI_API_KEY"] = "your-api-key-here"

    if "OPENAI_API_KEY" not in os.environ:
        print("Warning: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key before running the agent.")


def create_basic_agent(use_local_prompt=False):
    """Create a basic ReAct agent with Python REPL tool."""
    # Initialize the language model
    llm = ChatOpenAI(
        model="gpt-4",           # Use GPT-4 for better reasoning
        temperature=0            # Deterministic responses for debugging
    )

    # Create tools - starting with just Python execution
    tools = [PythonREPLTool()]

    # Option to use local ReAct prompt template
    if use_local_prompt:
        prompt_template = (
            "You are an intelligent agent that can reason step by step and use tools to solve problems.\n"
            "You have access to the following tools:\n"
            "{tools}\n\n"
            "When given a question, think out loud about what to do, then choose an action.\n"
            "Format:\n"
            "Question: {input}\n"
            "Thought: you should always think about what to do\n"
            "Action: the action to take, should be one of [{tool_names}]\n"
            "Action Input: the input to the action\n"
            "Observation: the result of the action\n"
            "... (this Thought/Action/Action Input/Observation can repeat N times)\n"
            "{agent_scratchpad}"
            "Thought: I now know the final answer\n"
            "Final Answer: the final answer to the original input question\n"
        )
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["input", "tool_names", "tools", "agent_scratchpad"]
        )
    else:
        from langchain import hub
        # Need LANGCHAIN_API_KEY set in .env file
        prompt = hub.pull("hwchase17/react")

    # Create the agent with ReAct reasoning capability
    agent = create_react_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    # Wrap in executor for actual execution
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,           # See the reasoning process
        max_iterations=5        # Prevent infinite loops
    )

    return agent_executor


def robust_agent_call(agent_executor, query, max_retries=3):
    """Execute agent query with error handling and retries."""
    for attempt in range(max_retries):
        try:
            return agent_executor.invoke({"input": query})
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_retries - 1:
                return {"output": f"Failed after {max_retries} attempts: {e}"}


if __name__ == "__main__":
    # Setup environment
    setup_environment()

    # Create the agent (set use_local_prompt=True to use local template)
    print("Creating ReAct agent...")
    agent_executor = create_basic_agent(use_local_prompt=False)

    # Simple test
    print("\nTesting with simple calculation:")
    result = robust_agent_call(agent_executor, "What is 25% of 1,380?")
    print("Result:", result['output'])

    # Advanced test
    print("\nTesting with quadratic equation:")
    result = robust_agent_call(agent_executor, "Solve the quadratic equation x² - 5x + 6 = 0")
    print("Result:", result['output'])