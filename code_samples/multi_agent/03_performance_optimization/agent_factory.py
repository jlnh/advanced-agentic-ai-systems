"""
Factory functions for creating optimized agents with different configurations.
"""

import os
from typing import Dict, Any, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_optimized_system():
    """Create fully optimized multi-agent system"""

    # Initialize agents with cost-conscious configuration
    agents = {
        "research": create_cost_optimized_agent("research", model="gpt-3.5-turbo"),
        "analysis": create_cost_optimized_agent("analysis", model="gpt-3.5-turbo"),
        "writing": create_cost_optimized_agent("writing", model="gpt-4"),
        "review": create_cost_optimized_agent("review", model="gpt-3.5-turbo")
    }

    # Create orchestrator with optimization settings
    from optimized_orchestrator import OptimizedOrchestrator

    orchestrator = OptimizedOrchestrator(
        agents=agents,
        max_workers=3,  # Optimal for most workloads
        max_retries=2,   # Balance reliability and cost
        cost_limit=0.50, # Per-request budget
        enable_caching=True
    )

    return orchestrator


def create_cost_optimized_agent(agent_type: str, model: str):
    """Create agent optimized for cost and performance"""

    try:
        # Try to import langchain components
        from langchain_openai import ChatOpenAI
        from langchain.prompts import PromptTemplate
        from langchain.agents import create_react_agent, AgentExecutor
        from langchain import hub

        llm = ChatOpenAI(
            model=model,
            temperature=0,
            max_tokens=500,  # Limit output length
            request_timeout=20,  # Prevent hanging requests
            api_key=os.getenv("OPENAI_API_KEY")
        )

        # Minimal tool set for each agent type
        tools = get_minimal_tools(agent_type)

        # Use a proper prompt template or fallback to default ReAct prompt
        try:
            # Try to get the default ReAct prompt from LangChain hub
            prompt = hub.pull("hwchase17/react")
        except Exception:
            # Fallback to a simple prompt template if hub is not available
            prompt_text = """You are a helpful assistant. Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
{agent_scratchpad}"""

            prompt = PromptTemplate(
                input_variables=["input", "agent_scratchpad"],
                template=prompt_text
            )

        # Create agent with proper prompt
        if tools:  # Only create ReAct agent if tools are available
            agent = create_react_agent(
                llm=llm,
                tools=tools,
                prompt=prompt
            )

            return AgentExecutor(
                agent=agent,
                tools=tools,
                max_iterations=3,  # Prevent runaway loops
                early_stopping_method="force",  # Stop at max iterations
                handle_parsing_errors=True
            )
        else:
            # For agents without tools, use simple LLM wrapper
            return SimpleLLMAgent(llm, agent_type)

    except ImportError as e:
        print(f"LangChain not available ({e}), using mock agent")
        # Fallback to mock agent if langchain not available
        return MockAgent(agent_type, model)
    except Exception as e:
        print(f"Error creating agent ({e}), using mock agent")
        return MockAgent(agent_type, model)


def get_minimal_tools(agent_type: str):
    """Return minimal tool set for agent type"""
    # Only essential tools to reduce token usage
    tool_map = {
        "research": [],  # Simplified - would include DuckDuckGoSearchTool
        "analysis": [],  # Simplified - would include PythonREPLTool
        "writing": [],   # Simplified - would include WriteFileTool
        "review": []     # Review uses no tools
    }
    return tool_map.get(agent_type, [])


def get_optimized_prompt(agent_type: str):
    """Get token-optimized prompt for agent type"""
    # Shorter, more focused prompts
    prompts = {
        "research": "Find and return facts. Be concise.",
        "analysis": "Analyze data. Return key insights only.",
        "writing": "Write clearly and concisely.",
        "review": "Check for errors. List issues if any."
    }
    return prompts.get(agent_type, "Complete the task efficiently.")


class SimpleLLMAgent:
    """Simple LLM wrapper for agents without tools"""

    def __init__(self, llm, agent_type: str):
        self.llm = llm
        self.agent_type = agent_type
        self.system_prompts = {
            "research": "You are a research assistant. Find and return facts. Be concise.",
            "analysis": "You are an analyst. Analyze data and return key insights only.",
            "writing": "You are a writer. Write clearly and concisely.",
            "review": "You are a reviewer. Check for errors and list issues if any."
        }

    def invoke(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke the LLM directly"""
        task_input = input_dict.get("input", "")
        system_prompt = self.system_prompts.get(self.agent_type, "You are a helpful assistant.")

        try:
            response = self.llm.invoke(f"{system_prompt}\n\nTask: {task_input}")
            return {
                "output": response.content if hasattr(response, 'content') else str(response)
            }
        except Exception as e:
            return {
                "output": f"Error processing task: {str(e)}"
            }


class MockAgent:
    """Mock agent for testing when langchain is not available"""

    def __init__(self, agent_type: str, model: str):
        self.agent_type = agent_type
        self.model = model

    def invoke(self, input_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Mock invoke method"""
        task_input = input_dict.get("input", "")

        # Simulate processing time
        import time
        time.sleep(1)

        # Mock response based on agent type
        responses = {
            "research": f"Research results for: {task_input}",
            "analysis": f"Analysis of: {task_input}",
            "writing": f"Written content for: {task_input}",
            "review": f"Review complete for: {task_input}"
        }

        return {
            "output": responses.get(self.agent_type, f"Task completed: {task_input}")
        }