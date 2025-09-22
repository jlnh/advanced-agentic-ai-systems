# src/agentic_ai/core/orchestration/supervisor.py
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import time
import asyncio

class TaskType(Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"

@dataclass
class Task:
    """Represents a single task in the execution plan"""
    id: str
    description: str
    agent_type: TaskType
    dependencies: List[str] = None
    priority: int = 1
    
    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class SupervisorAgent:
    """Basic orchestrator for multi-agent coordination"""
    
    def __init__(self, agents: Dict[str, Any]):
        self.agents = agents
        self.execution_history = []
        
    async def execute_task_sequence(self, tasks: List[Task]) -> Dict[str, Any]:
        """Execute tasks in sequence with dependency resolution"""
        results = {}
        
        # Sort tasks by dependencies and priority
        sorted_tasks = self._sort_tasks_by_dependencies(tasks)
        
        for task in sorted_tasks:
            print(f"🔄 Executing task: {task.id}")
            
            # Get appropriate agent
            agent = self._select_agent(task.agent_type)
            if not agent:
                results[task.id] = {
                    "success": False,
                    "error": f"No agent available for {task.agent_type}"
                }
                continue
            
            # Build context from dependencies
            context = self._build_context(task, results)
            
            # Execute task
            try:
                result = await agent.execute(task.description, context)
                results[task.id] = result
                print(f"✅ Task {task.id} completed")
            except Exception as e:
                results[task.id] = {
                    "success": False,
                    "error": str(e)
                }
                print(f"❌ Task {task.id} failed: {e}")
        
        return self._summarize_results(results)
    
    def _select_agent(self, task_type: TaskType):
        """Select appropriate agent for task type"""
        agent_mapping = {
            TaskType.RESEARCH: "research",
            TaskType.ANALYSIS: "analysis", 
            TaskType.WRITING: "writing"
        }
        
        agent_key = agent_mapping.get(task_type)
        return self.agents.get(agent_key)
    
    def _sort_tasks_by_dependencies(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks respecting dependencies"""
        sorted_tasks = []
        completed = set()
        remaining = tasks.copy()
        
        while remaining:
            # Find tasks with all dependencies completed
            ready_tasks = [
                task for task in remaining 
                if all(dep in completed for dep in task.dependencies)
            ]
            
            if not ready_tasks:
                # No tasks ready - possible circular dependency
                print("⚠️ Warning: Possible circular dependency detected")
                break
            
            # Sort by priority
            ready_tasks.sort(key=lambda t: t.priority)
            
            # Add first ready task
            next_task = ready_tasks[0]
            sorted_tasks.append(next_task)
            completed.add(next_task.id)
            remaining.remove(next_task)
        
        return sorted_tasks
    
    def _build_context(self, task: Task, results: Dict) -> Dict[str, Any]:
        """Build context from dependency results"""
        context = {}
        
        for dep_id in task.dependencies:
            if dep_id in results and results[dep_id].get("success"):
                context[f"result_{dep_id}"] = results[dep_id].get("output", "")
        
        return context
    
    def _summarize_results(self, results: Dict) -> Dict[str, Any]:
        """Summarize execution results"""
        successful_tasks = [
            task_id for task_id, result in results.items()
            if result.get("success", False)
        ]
        
        failed_tasks = [
            task_id for task_id, result in results.items()
            if not result.get("success", False)
        ]
        
        total_cost = sum(
            result.get("cost", 0) for result in results.values()
            if isinstance(result, dict)
        )
        
        # Combine successful outputs
        combined_output = "\n\n".join([
            f"Task {task_id}: {results[task_id].get('output', '')}"
            for task_id in successful_tasks
        ])
        
        return {
            "success": len(failed_tasks) == 0,
            "total_tasks": len(results),
            "successful_tasks": len(successful_tasks),
            "failed_tasks": len(failed_tasks),
            "total_cost": total_cost,
            "output": combined_output,
            "detailed_results": results
        }