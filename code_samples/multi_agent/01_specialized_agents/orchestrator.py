"""
Orchestrator for coordinating specialized agents.
"""

from typing import Dict, Any, List
from researcher_agent import create_researcher_agent
from analyst_agent import create_analyst_agent
from writer_agent import create_writer_agent


class SpecializedAgentSystem:
    """Coordinates specialized agents for complex tasks"""

    def __init__(self):
        self.researcher = create_researcher_agent()
        self.analyst = create_analyst_agent()
        self.writer = create_writer_agent()
        self.agents = {
            "research": self.researcher,
            "analyze": self.analyst,
            "write": self.writer
        }

    def classify_task(self, task: str) -> str:
        """Determine which agent should handle the task"""
        task_lower = task.lower()

        # Simple keyword-based classification
        # In production, use embeddings or LLM classification
        if any(word in task_lower for word in ["search", "find", "research", "latest"]):
            return "research"
        elif any(word in task_lower for word in ["analyze", "calculate", "compare", "pattern"]):
            return "analyze"
        elif any(word in task_lower for word in ["write", "create", "draft", "summarize"]):
            return "write"
        else:
            return "research"  # Default fallback

    def execute(self, task: str) -> Dict[str, Any]:
        """Execute task with appropriate specialist"""
        agent_type = self.classify_task(task)
        agent = self.agents[agent_type]

        print(f"Delegating to {agent_type} agent...")

        try:
            result = agent.invoke({"input": task})
            return {
                "success": True,
                "agent": agent_type,
                "result": result["output"],
                "metadata": {
                    "iterations": len(result.get("intermediate_steps", [])),
                    "tools_used": self._extract_tools_used(result)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "agent": agent_type,
                "error": str(e)
            }

    def _extract_tools_used(self, result: Dict) -> List[str]:
        """Extract which tools were actually used"""
        tools = []
        for step in result.get("intermediate_steps", []):
            if len(step) > 0:
                tools.append(step[0].tool)
        return list(set(tools))