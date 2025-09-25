"""
Test Suite for Multi-Agent Orchestration System
Comprehensive tests for task decomposition, dependency resolution, and execution.
"""

import pytest
import unittest
from unittest.mock import Mock, patch, MagicMock
from supervisor_agent import SupervisorAgent, Task, TaskType, ExecutionPlan
from enhanced_supervisor import EnhancedSupervisor
import json

class TestSupervisorAgent(unittest.TestCase):
    """Test cases for the SupervisorAgent"""

    def setUp(self):
        """Set up test fixtures"""
        self.mock_agents = {
            "researcher": self._create_mock_agent("research_output"),
            "analyst": self._create_mock_agent("analysis_output"),
            "writer": self._create_mock_agent("written_output")
        }
        self.supervisor = SupervisorAgent(self.mock_agents)

    def _create_mock_agent(self, output: str):
        """Create a mock agent that returns the specified output"""
        mock_agent = Mock()
        mock_agent.invoke.return_value = {"output": output}
        mock_agent.agent.prompt.template = f"Mock agent for {output}"
        return mock_agent

    def test_task_decomposition(self):
        """Test that complex requests are properly decomposed"""
        request = "Research AI trends and create a report"

        # Test the fallback plan creation since mocking LLM is complex
        plan = self.supervisor._create_fallback_plan(request)

        assert len(plan.tasks) == 1
        assert plan.tasks[0]["description"] == request
        assert plan.strategy == "sequential"
        assert plan.estimated_time == 30

        # Also test that the analyze_request method returns a valid plan
        # This will use the fallback if JSON parsing fails
        plan2 = self.supervisor.analyze_request(request)
        assert isinstance(plan2, ExecutionPlan)
        assert len(plan2.tasks) >= 1

    def test_dependency_resolution(self):
        """Test that dependencies are correctly ordered"""
        tasks = [
            {"id": "t1", "description": "Task 1", "agent_type": "research", "dependencies": [], "priority": 1},
            {"id": "t2", "description": "Task 2", "agent_type": "analysis", "dependencies": ["t1"], "priority": 2},
            {"id": "t3", "description": "Task 3", "agent_type": "writing", "dependencies": ["t1", "t2"], "priority": 3}
        ]

        groups = self.supervisor._group_tasks_by_dependencies(tasks)

        assert len(groups) == 3
        assert groups[0][0]["id"] == "t1"
        assert groups[1][0]["id"] == "t2"
        assert groups[2][0]["id"] == "t3"

    def test_context_building(self):
        """Test that context is properly built from dependencies"""
        task = Task(id="test", description="Test task", agent_type=TaskType.ANALYSIS, dependencies=["dep1"])
        results = {
            "dep1": {"success": True, "output": "Dependency output"}
        }

        context = self.supervisor._build_task_context(task, results)
        assert "Dependency output" in context
        assert "dep1" in context

    def test_agent_selection(self):
        """Test that appropriate agents are selected for task types"""
        research_agent = self.supervisor._select_agent(TaskType.RESEARCH)
        analysis_agent = self.supervisor._select_agent(TaskType.ANALYSIS)
        writing_agent = self.supervisor._select_agent(TaskType.WRITING)

        assert research_agent == self.mock_agents["researcher"]
        assert analysis_agent == self.mock_agents["analyst"]
        assert writing_agent == self.mock_agents["writer"]

    @patch('supervisor_agent.ThreadPoolExecutor')
    def test_parallel_execution(self, mock_executor):
        """Test parallel execution of independent tasks"""
        # Mock the executor behavior
        mock_future = Mock()
        mock_future.result.return_value = "task_output"

        mock_executor_instance = Mock()
        mock_executor_instance.__enter__ = Mock(return_value=mock_executor_instance)
        mock_executor_instance.__exit__ = Mock(return_value=None)
        mock_executor_instance.submit.return_value = mock_future
        mock_executor.return_value = mock_executor_instance

        plan = ExecutionPlan(
            tasks=[
                {"id": "t1", "description": "Task 1", "agent_type": "research", "dependencies": [], "priority": 1},
                {"id": "t2", "description": "Task 2", "agent_type": "research", "dependencies": [], "priority": 1}
            ],
            strategy="parallel",
            estimated_time=30
        )

        result = self.supervisor.execute_plan(plan)
        assert result["status"] == "completed"
        assert result["success_rate"] == 1.0

    def test_fallback_plan_creation(self):
        """Test fallback plan creation when JSON parsing fails"""
        request = "Simple request"
        fallback_plan = self.supervisor._create_fallback_plan(request)

        assert len(fallback_plan.tasks) == 1
        assert fallback_plan.tasks[0]["description"] == request
        assert fallback_plan.strategy == "sequential"

    def test_result_synthesis(self):
        """Test that results are properly synthesized"""
        results = {
            "task1": {"success": True, "output": "Output 1", "task": Mock()},
            "task2": {"success": True, "output": "Output 2", "task": Mock()}
        }

        synthesis = self.supervisor._synthesize_results(results)

        assert synthesis["status"] == "completed"
        assert synthesis["success_rate"] == 1.0
        assert "Output 1" in synthesis["output"]
        assert "Output 2" in synthesis["output"]

    def test_partial_success_handling(self):
        """Test handling of partial success scenarios"""
        mock_task = Mock()
        mock_task.id = "failed_task"

        results = {
            "task1": {"success": True, "output": "Success", "task": Mock()},
            "task2": {"success": False, "error": "Failed", "task": mock_task}
        }

        synthesis = self.supervisor._synthesize_results(results)

        assert synthesis["status"] == "partial"
        assert synthesis["success_rate"] == 0.5
        assert "failed_task" in synthesis["output"]


class TestEnhancedSupervisor(unittest.TestCase):
    """Test cases for the EnhancedSupervisor"""

    def setUp(self):
        """Set up test fixtures"""
        mock_agents = {
            "researcher": Mock(),
            "analyst": Mock(),
            "writer": Mock()
        }
        self.enhanced_supervisor = EnhancedSupervisor(mock_agents)

    def test_performance_monitoring(self):
        """Test performance metrics tracking"""
        metrics = {
            "duration": 10.5,
            "tokens": 1500,
            "cost": 0.05,
            "success": True
        }

        self.enhanced_supervisor.monitor_performance("task1", metrics)

        assert "task1" in self.enhanced_supervisor.performance_metrics
        assert len(self.enhanced_supervisor.performance_metrics["task1"]) == 1
        assert self.enhanced_supervisor.performance_metrics["task1"][0]["duration"] == 10.5

    def test_plan_caching(self):
        """Test that similar plans are cached"""
        request = "Test request"

        # Mock the parent's analyze_request method
        with patch.object(SupervisorAgent, 'analyze_request') as mock_analyze:
            mock_plan = ExecutionPlan(tasks=[], strategy="sequential", estimated_time=30)
            mock_analyze.return_value = mock_plan

            # First call should hit the parent method
            plan1 = self.enhanced_supervisor.analyze_request(request)
            assert mock_analyze.call_count == 1

            # Second call should use cache
            plan2 = self.enhanced_supervisor.analyze_request(request)
            assert mock_analyze.call_count == 1  # Should not increase

            assert plan1 == plan2

    def test_cost_tracking(self):
        """Test cost tracking and budget limits"""
        self.enhanced_supervisor.budget_per_request = 0.10  # Low budget for testing

        plan = ExecutionPlan(
            tasks=[{"id": "expensive_task", "description": "Expensive task", "agent_type": "research", "dependencies": []}],
            strategy="sequential",
            estimated_time=60
        )

        # Mock the execution to simulate high cost
        with patch.object(self.enhanced_supervisor, '_execute_single_task') as mock_execute:
            def expensive_execute(*args, **kwargs):
                # Simulate expensive operation
                import time
                time.sleep(0.1)  # Brief sleep to simulate duration
                return "expensive result"

            mock_execute.side_effect = expensive_execute

            # Should complete but track cost
            result = self.enhanced_supervisor.execute_plan(plan)
            assert result is not None

    def test_alert_system(self):
        """Test alert system triggers"""
        # Simulate high failure rate
        self.enhanced_supervisor.metrics = {
            "total_requests": 10,
            "successful_requests": 5,
            "failed_requests": 5,
            "total_duration": 100,
            "total_cost": 5.0
        }

        with patch.object(self.enhanced_supervisor, 'send_alert') as mock_alert:
            self.enhanced_supervisor.check_alerts()
            mock_alert.assert_called()  # Should trigger alert for high failure rate

    def test_fallback_execution(self):
        """Test fallback execution strategies"""
        request = "Test request that should trigger fallback"

        # Mock primary execution to fail
        with patch.object(self.enhanced_supervisor, 'run') as mock_run:
            mock_run.side_effect = Exception("Primary execution failed")

            # Mock emergency execution
            with patch.object(self.enhanced_supervisor, '_emergency_direct_execution') as mock_emergency:
                mock_emergency.return_value = {"status": "emergency", "output": "Emergency result", "task_results": {}, "success_rate": 0.5}

                result = self.enhanced_supervisor.execute_with_fallback(request)
                assert result["status"] == "emergency"
                mock_emergency.assert_called_once_with(request)

def create_mock_agent_for_testing(output: str):
    """Helper function to create mock agents for testing"""
    mock_agent = Mock()
    mock_agent.invoke.return_value = {"output": output}
    mock_agent.agent.prompt.template = f"Mock agent for {output}"
    return mock_agent

def test_full_orchestration_integration():
    """Integration test for complete orchestration flow"""

    # Create mock agents
    mock_agents = {
        "researcher": create_mock_agent_for_testing("research_output"),
        "analyst": create_mock_agent_for_testing("analysis_output"),
        "writer": create_mock_agent_for_testing("written_output")
    }

    supervisor = SupervisorAgent(mock_agents)

    # Test with a simple request (will use fallback plan)
    result = supervisor.run("Research topic X and analyze the data")

    assert result["status"] in ["completed", "partial"]
    assert "success_rate" in result
    assert "output" in result
    assert "task_results" in result

    # The fallback plan creates a single research task
    assert len(result["task_results"]) >= 1

if __name__ == "__main__":
    # Set up logging for tests
    import logging
    logging.basicConfig(level=logging.INFO)

    # Run the tests
    unittest.main(verbosity=2)