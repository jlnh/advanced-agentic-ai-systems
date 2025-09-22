from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from langchain.agents import AgentExecutor
from langchain.schema import BaseMessage
import time
import logging

class BaseAgent(ABC):
    """Base class for all specialized agents"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.executor: Optional[AgentExecutor] = None
        self.logger = logging.getLogger(f"agent.{name}")
        
    @abstractmethod
    async def execute(self, task: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute a task and return results"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """Return list of agent capabilities"""
        pass
    
    def log_execution(self, task: str, result: Dict[str, Any], duration: float):
        """Log execution details"""
        self.logger.info(
            f"Executed task in {duration:.2f}s",
            extra={
                "agent": self.name,
                "task_preview": task[:100],
                "success": result.get("success", False),
                "cost": result.get("cost", 0)
            }
        )
