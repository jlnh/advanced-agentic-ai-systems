"""
Supervisor Agent for Multi-Agent Orchestration
Implements sophisticated task decomposition, delegation, and quality assurance.
"""

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import json
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Define task types and execution strategies
class TaskType(Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"
    REVIEW = "review"

class ExecutionStrategy(Enum):
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HYBRID = "hybrid"

@dataclass
class Task:
    """Represents a single task in the execution plan"""
    id: str
    description: str
    agent_type: TaskType
    dependencies: List[str] = None  # IDs of tasks this depends on
    priority: int = 1
    max_retries: int = 2
    timeout: int = 30

    def __post_init__(self):
        if self.dependencies is None:
            self.dependencies = []

class ExecutionPlan(BaseModel):
    """Structured execution plan created by supervisor"""
    tasks: List[Dict[str, Any]] = Field(description="List of tasks to execute")
    strategy: str = Field(description="Execution strategy: sequential, parallel, or hybrid")
    estimated_time: int = Field(description="Estimated completion time in seconds")

class SupervisorAgent:
    """
    Orchestrates multi-agent systems with sophisticated planning and execution.
    Handles task decomposition, delegation, and quality assurance.
    """

    def __init__(self, specialized_agents: Dict[str, AgentExecutor]):
        self.agents = specialized_agents
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.supervisor_executor = self._create_supervisor()
        self.execution_history = []

    def _create_supervisor(self):
        """Creates the supervisor agent with planning capabilities"""
        # The supervisor doesn't need AgentExecutor since it only does planning
        # We'll use the LLM directly for planning
        return None

    def analyze_request(self, request: str) -> ExecutionPlan:
        """
        Analyzes request and creates execution plan.
        This is where the supervisor's intelligence shines.
        """

        # Get agent descriptions for context
        agent_descriptions = self._get_agent_descriptions()

        # Create planning prompt
        planning_prompt = f"""
        Analyze this request and create an execution plan:
        Request: {request}

        Available agents: {agent_descriptions}

        Return a JSON execution plan with:
        - tasks: array of task objects (id, description, agent_type, dependencies, priority)
        - strategy: "sequential", "parallel", or "hybrid"
        - estimated_time: total seconds

        Example format:
        {{
            "tasks": [
                {{"id": "task1", "description": "...", "agent_type": "research", "dependencies": [], "priority": 1}},
                {{"id": "task2", "description": "...", "agent_type": "analysis", "dependencies": ["task1"], "priority": 2}}
            ],
            "strategy": "hybrid",
            "estimated_time": 45
        }}
        """

        # Use structured output parsing
        response = self.llm.invoke(planning_prompt).content

        try:
            plan_data = json.loads(response)
            return ExecutionPlan(**plan_data)
        except json.JSONDecodeError:
            # Fallback to simple sequential plan
            return self._create_fallback_plan(request)

    def _create_fallback_plan(self, request: str) -> ExecutionPlan:
        """Creates a simple fallback plan if parsing fails"""
        return ExecutionPlan(
            tasks=[
                {"id": "task1", "description": request, "agent_type": "research",
                 "dependencies": [], "priority": 1}
            ],
            strategy="sequential",
            estimated_time=30
        )

    def _get_agent_descriptions(self) -> str:
        """Get descriptions of available agents"""
        descriptions = [
            "- researcher: Expert research agent that can search the web for information and compile findings",
            "- analyst: Data analysis specialist that interprets research findings and provides insights",
            "- writer: Content creation expert that transforms analysis into well-structured reports"
        ]
        return "\n".join(descriptions)

    def execute_plan(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """
        Executes the plan using appropriate strategy.
        This is the core orchestration logic.
        """

        print(f"\n📋 Executing plan with {plan.strategy} strategy")
        print(f"⏱️  Estimated time: {plan.estimated_time}s")

        if plan.strategy == "sequential":
            return self._execute_sequential(plan)
        elif plan.strategy == "parallel":
            return self._execute_parallel(plan)
        else:  # hybrid
            return self._execute_hybrid(plan)

    def _execute_sequential(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Execute tasks one after another"""
        results = {}
        context = {}  # Accumulate context for dependent tasks

        for task_data in plan.tasks:
            task = Task(**task_data)
            print(f"\n▶️  Executing {task.id}: {task.description}")

            # Add context from dependencies
            task_context = self._build_task_context(task, results)

            # Execute with appropriate agent
            agent = self._select_agent(task.agent_type)

            try:
                result = self._execute_single_task(
                    agent,
                    task,
                    task_context
                )
                results[task.id] = {
                    "success": True,
                    "output": result,
                    "task": task
                }
                print(f"✅ {task.id} completed successfully")

            except Exception as e:
                results[task.id] = {
                    "success": False,
                    "error": str(e),
                    "task": task
                }
                print(f"❌ {task.id} failed: {e}")

                # Decide whether to continue or abort
                if task.priority == 1:  # Critical task
                    break

        return self._synthesize_results(results)

    def _execute_parallel(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Execute independent tasks in parallel"""
        results = {}

        # Group tasks by dependency level
        task_groups = self._group_tasks_by_dependencies(plan.tasks)

        for level, tasks in enumerate(task_groups):
            print(f"\n🔄 Executing parallel group {level + 1}")

            # Execute tasks in this level in parallel
            with ThreadPoolExecutor(max_workers=3) as executor:
                futures = {}

                for task_data in tasks:
                    task = Task(**task_data)
                    agent = self._select_agent(task.agent_type)
                    context = self._build_task_context(task, results)

                    future = executor.submit(
                        self._execute_single_task,
                        agent,
                        task,
                        context
                    )
                    futures[future] = task

                # Collect results
                for future in futures:
                    task = futures[future]
                    try:
                        result = future.result(timeout=task.timeout)
                        results[task.id] = {
                            "success": True,
                            "output": result,
                            "task": task
                        }
                        print(f"✅ {task.id} completed")
                    except Exception as e:
                        results[task.id] = {
                            "success": False,
                            "error": str(e),
                            "task": task
                        }
                        print(f"❌ {task.id} failed: {e}")

        return self._synthesize_results(results)

    def _execute_hybrid(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """
        Execute with mixed sequential and parallel strategy.
        This is the most sophisticated approach.
        """
        results = {}

        # Analyze task graph to identify parallel opportunities
        task_graph = self._build_dependency_graph(plan.tasks)
        execution_stages = self._calculate_execution_stages(task_graph)

        for stage_num, stage_tasks in enumerate(execution_stages):
            print(f"\n🎯 Stage {stage_num + 1}: {len(stage_tasks)} tasks")

            if len(stage_tasks) == 1:
                # Single task - execute sequentially
                task = stage_tasks[0]
                agent = self._select_agent(task.agent_type)
                context = self._build_task_context(task, results)

                try:
                    result = self._execute_single_task(agent, task, context)
                    results[task.id] = {
                        "success": True,
                        "output": result,
                        "task": task
                    }
                except Exception as e:
                    results[task.id] = {
                        "success": False,
                        "error": str(e),
                        "task": task
                    }
            else:
                # Multiple tasks - execute in parallel
                with ThreadPoolExecutor(max_workers=min(3, len(stage_tasks))) as executor:
                    futures = {}

                    for task in stage_tasks:
                        agent = self._select_agent(task.agent_type)
                        context = self._build_task_context(task, results)

                        future = executor.submit(
                            self._execute_single_task,
                            agent,
                            task,
                            context
                        )
                        futures[future] = task

                    for future in futures:
                        task = futures[future]
                        try:
                            result = future.result(timeout=task.timeout)
                            results[task.id] = {
                                "success": True,
                                "output": result,
                                "task": task
                            }
                        except Exception as e:
                            results[task.id] = {
                                "success": False,
                                "error": str(e),
                                "task": task
                            }

        return self._synthesize_results(results)

    def _execute_single_task(
        self,
        agent: AgentExecutor,
        task: Task,
        context: str
    ) -> str:
        """Execute a single task with retry logic"""

        # Prepare input with context
        if context:
            full_input = f"Context from previous tasks:\n{context}\n\nTask: {task.description}"
        else:
            full_input = task.description

        # Try execution with retries
        last_error = None
        for attempt in range(task.max_retries):
            try:
                result = agent.invoke(
                    {"input": full_input}
                )
                return result.get("output", "")

            except Exception as e:
                last_error = e
                if attempt < task.max_retries - 1:
                    print(f"  ⚠️  Retry {attempt + 1} for {task.id}")
                    # Add exponential backoff
                    time.sleep(2 ** attempt)

        raise last_error

    def _select_agent(self, task_type: TaskType) -> AgentExecutor:
        """Select appropriate agent for task type"""
        mapping = {
            TaskType.RESEARCH: "researcher",
            TaskType.ANALYSIS: "analyst",
            TaskType.WRITING: "writer"
        }

        agent_name = mapping.get(task_type, "researcher")
        return self.agents.get(agent_name)

    def _build_task_context(self, task: Task, results: Dict) -> str:
        """Build context from dependent task results"""
        if not task.dependencies:
            return ""

        context_parts = []
        for dep_id in task.dependencies:
            if dep_id in results and results[dep_id]["success"]:
                context_parts.append(
                    f"Results from {dep_id}:\n{results[dep_id]['output']}"
                )

        return "\n\n".join(context_parts)

    def _group_tasks_by_dependencies(self, tasks: List[Dict]) -> List[List[Dict]]:
        """Group tasks into levels based on dependencies"""
        levels = []
        completed = set()
        remaining = tasks.copy()

        while remaining:
            current_level = []

            for task in remaining[:]:
                task_obj = Task(**task)
                # Check if all dependencies are completed
                if all(dep in completed for dep in task_obj.dependencies):
                    current_level.append(task)
                    remaining.remove(task)

            if not current_level:
                # Circular dependency or error
                break

            levels.append(current_level)
            for task in current_level:
                completed.add(task["id"])

        return levels

    def _build_dependency_graph(self, tasks: List[Dict]) -> Dict[str, Task]:
        """Build dependency graph for execution planning"""
        graph = {}
        for task_data in tasks:
            task = Task(**task_data)
            graph[task.id] = task
        return graph

    def _calculate_execution_stages(self, graph: Dict[str, Task]) -> List[List[Task]]:
        """Calculate optimal execution stages respecting dependencies"""
        stages = []
        executed = set()

        while len(executed) < len(graph):
            stage = []

            for task_id, task in graph.items():
                if task_id not in executed:
                    # Check if all dependencies are executed
                    if all(dep in executed for dep in task.dependencies):
                        stage.append(task)

            if not stage:
                break  # No more tasks can be executed

            stages.append(stage)
            for task in stage:
                executed.add(task.id)

        return stages

    def _synthesize_results(self, results: Dict) -> Dict[str, Any]:
        """Synthesize individual results into final output"""

        # Check overall success
        all_success = all(r["success"] for r in results.values())

        # Compile outputs
        successful_outputs = [
            r["output"] for r in results.values()
            if r["success"]
        ]

        # Create summary
        if all_success:
            final_output = "\n\n".join(successful_outputs)
            status = "completed"
        else:
            failed_tasks = [
                r["task"].id for r in results.values()
                if not r["success"]
            ]
            final_output = f"Partial completion. Failed tasks: {failed_tasks}"
            status = "partial"

        return {
            "status": status,
            "output": final_output,
            "task_results": results,
            "success_rate": sum(1 for r in results.values() if r["success"]) / len(results)
        }

    def run(self, request: str) -> Dict[str, Any]:
        """Main entry point for orchestrated execution"""

        print(f"\n🎯 New Request: {request}\n")

        # Step 1: Analyze and plan
        print("📊 Analyzing request and creating execution plan...")
        plan = self.analyze_request(request)

        # Step 2: Execute plan
        print(f"\n🚀 Executing plan with {len(plan.tasks)} tasks")
        results = self.execute_plan(plan)

        # Step 3: Log for analysis
        self.execution_history.append({
            "request": request,
            "plan": plan,
            "results": results
        })

        return results