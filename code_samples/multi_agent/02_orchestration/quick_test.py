"""
Quick Test of Multi-Agent Orchestration System
Demonstrates the system architecture without making expensive API calls.
"""

from supervisor_agent import SupervisorAgent, Task, TaskType, ExecutionPlan
from typing import Dict, Any
import json

class MockAgent:
    """Mock agent for testing without API calls"""

    def __init__(self, agent_type: str):
        self.agent_type = agent_type

    def invoke(self, inputs: Dict[str, Any]) -> Dict[str, str]:
        """Mock invoke method that returns sample outputs"""

        sample_outputs = {
            "researcher": f"[MOCK RESEARCH] Based on web search about '{inputs['input'][:50]}...', "
                         f"I found key findings including market trends, statistics, and recent developments.",

            "analyst": f"[MOCK ANALYSIS] Analysis of the research shows significant patterns and insights. "
                      f"Key factors include growth trends, market opportunities, and strategic implications.",

            "writer": f"[MOCK REPORT] **Executive Summary**\n\n"
                     f"This report presents findings on '{inputs['input'][:50]}...'\n\n"
                     f"**Key Findings:**\n- Major trend 1\n- Important insight 2\n- Strategic recommendation 3\n\n"
                     f"**Conclusion:** The analysis reveals significant opportunities and actionable insights."
        }

        return {"output": sample_outputs.get(self.agent_type, "Mock output")}

class MockSupervisor(SupervisorAgent):
    """Mock supervisor that creates realistic plans without API calls"""

    def analyze_request(self, request: str) -> ExecutionPlan:
        """Create a realistic execution plan based on request complexity"""

        # Simple pattern matching for demonstration
        if "parallel" in request.lower() or "three topics" in request.lower():
            # Complex parallel + sequential pattern
            return ExecutionPlan(
                tasks=[
                    {"id": "research_topic_1", "description": "Research quantum computing",
                     "agent_type": "research", "dependencies": [], "priority": 1},
                    {"id": "research_topic_2", "description": "Research fusion energy",
                     "agent_type": "research", "dependencies": [], "priority": 1},
                    {"id": "research_topic_3", "description": "Research brain-computer interfaces",
                     "agent_type": "research", "dependencies": [], "priority": 1},
                    {"id": "comparative_analysis", "description": "Compare commercial potential",
                     "agent_type": "analysis", "dependencies": ["research_topic_1", "research_topic_2", "research_topic_3"], "priority": 2},
                    {"id": "executive_brief", "description": "Create executive briefing",
                     "agent_type": "writing", "dependencies": ["comparative_analysis"], "priority": 3}
                ],
                strategy="hybrid",
                estimated_time=90
            )
        elif "analyze" in request.lower() and "write" in request.lower():
            # Sequential research -> analysis -> writing
            return ExecutionPlan(
                tasks=[
                    {"id": "research_task", "description": f"Research: {request[:60]}...",
                     "agent_type": "research", "dependencies": [], "priority": 1},
                    {"id": "analysis_task", "description": "Analyze research findings",
                     "agent_type": "analysis", "dependencies": ["research_task"], "priority": 2},
                    {"id": "writing_task", "description": "Create final report",
                     "agent_type": "writing", "dependencies": ["analysis_task"], "priority": 3}
                ],
                strategy="sequential",
                estimated_time=60
            )
        else:
            # Simple research task
            return ExecutionPlan(
                tasks=[
                    {"id": "simple_research", "description": request,
                     "agent_type": "research", "dependencies": [], "priority": 1}
                ],
                strategy="sequential",
                estimated_time=30
            )

def demonstrate_orchestration():
    """Demonstrate the orchestration system with mock agents"""

    print("🚀 Multi-Agent Orchestration System - Quick Demonstration")
    print("=" * 60)

    # Create mock agents
    mock_agents = {
        "researcher": MockAgent("researcher"),
        "analyst": MockAgent("analyst"),
        "writer": MockAgent("writer")
    }

    # Create mock supervisor
    supervisor = MockSupervisor(mock_agents)

    # Test scenarios
    test_scenarios = [
        {
            "name": "Simple Research Task",
            "request": "Find information about renewable energy trends in 2024"
        },
        {
            "name": "Multi-Step Analysis",
            "request": "Research the top 3 AI companies, analyze their market positions, and create an investment summary"
        },
        {
            "name": "Complex Parallel Workflow",
            "request": """Research these three topics in parallel:
            1. Current state of quantum computing
            2. Latest developments in fusion energy
            3. Progress in brain-computer interfaces

            Then analyze which has the most commercial potential in the next 5 years,
            and write an executive briefing for investors."""
        }
    ]

    for i, scenario in enumerate(test_scenarios, 1):
        print(f"\n🎯 TEST {i}: {scenario['name']}")
        print("-" * 50)
        print(f"Request: {scenario['request'][:100]}{'...' if len(scenario['request']) > 100 else ''}")

        try:
            # Run orchestration
            result = supervisor.run(scenario["request"])

            # Display results
            print(f"\n📊 Results:")
            print(f"  Status: {result['status']}")
            print(f"  Success Rate: {result['success_rate']*100:.1f}%")
            print(f"  Tasks Completed: {len(result['task_results'])}")

            # Show task breakdown
            print(f"\n📋 Task Execution Details:")
            for task_id, task_result in result['task_results'].items():
                status = "✅" if task_result['success'] else "❌"
                agent_type = task_result['task'].agent_type if hasattr(task_result['task'], 'agent_type') else 'unknown'
                description = task_result['task'].description if hasattr(task_result['task'], 'description') else 'No description'
                print(f"  {status} {task_id} ({agent_type}): {description[:50]}...")

            # Show sample output
            print(f"\n📄 Sample Output:")
            preview = result['output'][:300] + "..." if len(result['output']) > 300 else result['output']
            print(f"  {preview}")

        except Exception as e:
            print(f"❌ Error: {e}")

        print("\n" + "=" * 60)

def demonstrate_execution_strategies():
    """Demonstrate different execution strategies"""

    print("\n🔄 Execution Strategy Demonstration")
    print("=" * 50)

    mock_agents = {
        "researcher": MockAgent("researcher"),
        "analyst": MockAgent("analyst"),
        "writer": MockAgent("writer")
    }

    supervisor = MockSupervisor(mock_agents)

    strategies = [
        ("Sequential", [
            {"id": "task1", "description": "Research topic", "agent_type": "research", "dependencies": []},
            {"id": "task2", "description": "Analyze findings", "agent_type": "analysis", "dependencies": ["task1"]},
            {"id": "task3", "description": "Write report", "agent_type": "writing", "dependencies": ["task2"]}
        ]),
        ("Parallel", [
            {"id": "research_a", "description": "Research topic A", "agent_type": "research", "dependencies": []},
            {"id": "research_b", "description": "Research topic B", "agent_type": "research", "dependencies": []},
            {"id": "research_c", "description": "Research topic C", "agent_type": "research", "dependencies": []}
        ]),
        ("Hybrid", [
            {"id": "research_1", "description": "Research phase 1", "agent_type": "research", "dependencies": []},
            {"id": "research_2", "description": "Research phase 2", "agent_type": "research", "dependencies": []},
            {"id": "synthesis", "description": "Synthesize findings", "agent_type": "analysis", "dependencies": ["research_1", "research_2"]},
            {"id": "final_report", "description": "Create final report", "agent_type": "writing", "dependencies": ["synthesis"]}
        ])
    ]

    for strategy_name, tasks in strategies:
        print(f"\n🎯 {strategy_name} Strategy:")

        plan = ExecutionPlan(
            tasks=tasks,
            strategy=strategy_name.lower(),
            estimated_time=45
        )

        print(f"  Tasks: {len(plan.tasks)}")
        print(f"  Strategy: {plan.strategy}")

        # Show task dependencies
        for task in plan.tasks:
            deps = task.get("dependencies", [])
            dep_str = f" (depends on: {', '.join(deps)})" if deps else " (no dependencies)"
            print(f"    - {task['id']}: {task['description'][:40]}...{dep_str}")

if __name__ == "__main__":
    print("🔧 Multi-Agent Orchestration - Quick Test Suite")
    print("This demonstrates the system architecture without making API calls.\n")

    # Main demonstration
    demonstrate_orchestration()

    # Strategy demonstration
    demonstrate_execution_strategies()

    print("\n✅ Quick test completed successfully!")
    print("\nTo run with real API calls, use: python orchestration_example.py")
    print("Make sure to set your OPENAI_API_KEY in the .env file first.")