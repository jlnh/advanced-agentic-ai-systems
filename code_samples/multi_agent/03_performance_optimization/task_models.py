"""
Task definitions and data models for the multi-agent system.
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    id: str
    description: str
    agent_type: str
    dependencies: List[str] = field(default_factory=list)
    priority: int = 3  # 1=critical, 5=optional
    timeout: int = 30
    max_tokens: int = 1000
    model_override: str = None  # Use specific model for cost optimization
    cacheable: bool = True