"""
Cost monitoring and control for multi-agent systems.
Implements various strategies to stay within budget.
"""

import time
import threading
from typing import Dict, List


class CostController:
    """
    Monitors and controls costs in real-time.
    Implements various strategies to stay within budget.
    """

    def __init__(self, cost_limit: float):
        self.cost_limit = cost_limit
        self.current_cost = 0.0
        self.cost_by_agent = {}
        self.cost_history = []
        self.lock = threading.Lock()

    def add_cost(self, cost: float, agent_type: str = None):
        """Record cost and check limits"""
        with self.lock:
            self.current_cost += cost
            self.cost_history.append((time.time(), cost))

            if agent_type:
                self.cost_by_agent[agent_type] = \
                    self.cost_by_agent.get(agent_type, 0) + cost

    def can_proceed(self) -> bool:
        """Check if we can proceed within budget"""
        return self.current_cost < self.cost_limit

    def get_remaining_budget(self) -> float:
        """Get remaining budget"""
        return max(0, self.cost_limit - self.current_cost)

    def get_cost_breakdown(self) -> Dict:
        """Get detailed cost breakdown"""
        return {
            "total": self.current_cost,
            "remaining": self.get_remaining_budget(),
            "by_agent": self.cost_by_agent,
            "average_per_task": self.current_cost / len(self.cost_history)
                                if self.cost_history else 0
        }

    def suggest_optimizations(self) -> List[str]:
        """Suggest cost optimization strategies"""
        suggestions = []

        if self.current_cost > self.cost_limit * 0.8:
            suggestions.append("Consider using GPT-3.5 for simple tasks")

        # Find expensive agents
        expensive_agents = [
            agent for agent, cost in self.cost_by_agent.items()
            if cost > self.current_cost * 0.4
        ]
        if expensive_agents:
            suggestions.append(f"Optimize prompts for: {', '.join(expensive_agents)}")

        return suggestions