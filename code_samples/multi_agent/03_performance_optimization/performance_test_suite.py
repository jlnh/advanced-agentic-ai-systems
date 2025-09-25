"""
Comprehensive testing for optimization validation.
Run these tests to ensure your optimizations work.
"""

import os
import time
from typing import List, Dict
from dotenv import load_dotenv

from optimized_orchestrator import OptimizedOrchestrator
from task_models import Task

# Load environment variables
load_dotenv()


class PerformanceTestSuite:
    """
    Comprehensive testing for optimization validation.
    Run these tests to ensure your optimizations work.
    """

    def __init__(self, orchestrator: OptimizedOrchestrator):
        self.orchestrator = orchestrator
        self.test_results = []

    def run_all_tests(self):
        """Run complete test suite"""

        print("\n🧪 Running Performance Test Suite\n")

        self.test_parallel_speedup()
        self.test_error_recovery()
        self.test_cost_control()
        self.test_cache_effectiveness()
        self.test_circuit_breaker()

        self._print_summary()

    def test_parallel_speedup(self):
        """Test parallel execution performance"""

        print("📊 Testing Parallel Speedup...")

        # Create independent tasks
        tasks = [
            Task(f"task_{i}", f"Process item {i}", "research", [])
            for i in range(5)
        ]

        # Sequential baseline
        start = time.time()
        for task in tasks:
            self.orchestrator._execute_task_with_monitoring(task, "")
        sequential_time = time.time() - start

        # Parallel execution
        start = time.time()
        self.orchestrator.execute_parallel(tasks)
        parallel_time = time.time() - start

        speedup = sequential_time / parallel_time if parallel_time > 0 else 1

        self.test_results.append({
            "test": "Parallel Speedup",
            "passed": speedup > 1.5,  # Expect at least 1.5x speedup
            "details": f"Speedup: {speedup:.1f}x (Sequential: {sequential_time:.1f}s, Parallel: {parallel_time:.1f}s)"
        })

    def test_error_recovery(self):
        """Test error handling and retry logic"""

        print("🔄 Testing Error Recovery...")

        # Create task that fails initially
        failing_task = Task("fail_test", "This will fail once", "research", [])

        # Mock agent to fail then succeed
        original_agent = self.orchestrator.agents.get("research")

        call_count = [0]

        def mock_invoke(input_dict):
            call_count[0] += 1
            if call_count[0] == 1:
                raise Exception("Simulated failure")
            return {"output": "Success after retry"}

        if hasattr(original_agent, 'invoke'):
            original_invoke = original_agent.invoke
            original_agent.invoke = mock_invoke

            result = self.orchestrator._execute_task_with_monitoring(failing_task, "")

            # Restore original method
            original_agent.invoke = original_invoke

            self.test_results.append({
                "test": "Error Recovery",
                "passed": result["success"] and result["attempts"] >= 2,
                "details": f"Recovered after {result.get('attempts', 0)} attempts"
            })
        else:
            self.test_results.append({
                "test": "Error Recovery",
                "passed": False,
                "details": "Could not test - agent doesn't have invoke method"
            })

    def test_cost_control(self):
        """Test cost limiting functionality"""

        print("💰 Testing Cost Control...")

        # Set very low cost limit
        original_limit = self.orchestrator.cost_controller.cost_limit
        self.orchestrator.cost_controller.cost_limit = 0.01

        # Try to execute expensive tasks
        expensive_tasks = [
            Task(f"expensive_{i}", f"Complex analysis {i}", "analysis", [])
            for i in range(10)
        ]

        results = self.orchestrator.execute_parallel(expensive_tasks)

        # Count how many were skipped due to cost
        skipped = sum(1 for r in results.values()
                     if r.get("error") == "Cost limit exceeded")

        self.test_results.append({
            "test": "Cost Control",
            "passed": skipped > 0,
            "details": f"Blocked {skipped} tasks due to cost limits"
        })

        # Reset cost limit
        self.orchestrator.cost_controller.cost_limit = original_limit

    def test_cache_effectiveness(self):
        """Test caching reduces redundant calls"""

        print("📦 Testing Cache Effectiveness...")

        # Execute same task multiple times
        identical_task = Task("cache_test", "Find information about Python", "research", [])

        # Reset cache stats
        if self.orchestrator.result_cache:
            initial_hits = self.orchestrator.metrics.cache_hits
            initial_misses = self.orchestrator.metrics.cache_misses

            # First execution (cache miss)
            result1 = self.orchestrator._execute_task_with_monitoring(identical_task, "")

            # Second execution (should hit cache if implemented correctly)
            result2 = self.orchestrator._execute_stage_parallel([identical_task], {})

            cache_worked = self.orchestrator.metrics.cache_hits > initial_hits

            self.test_results.append({
                "test": "Cache Effectiveness",
                "passed": cache_worked,
                "details": f"Cache hits: {self.orchestrator.metrics.cache_hits}, misses: {self.orchestrator.metrics.cache_misses}"
            })
        else:
            self.test_results.append({
                "test": "Cache Effectiveness",
                "passed": False,
                "details": "Cache not enabled"
            })

    def test_circuit_breaker(self):
        """Test circuit breaker prevents cascade failures"""

        print("⚡ Testing Circuit Breaker...")

        # Force multiple failures
        for i in range(4):
            self.orchestrator.circuit_breaker.record_failure("test_agent")

        # Check if circuit is open
        is_open = self.orchestrator.circuit_breaker.is_open("test_agent")

        # Record successes to close circuit
        # Set state to half-open first
        self.orchestrator.circuit_breaker.state["test_agent"] = "half_open"
        self.orchestrator.circuit_breaker.successes["test_agent"] = 0

        for i in range(3):
            self.orchestrator.circuit_breaker.record_success("test_agent")

        # Check if circuit recovered
        is_closed = not self.orchestrator.circuit_breaker.is_open("test_agent")

        self.test_results.append({
            "test": "Circuit Breaker",
            "passed": is_open and is_closed,
            "details": f"Circuit opened after failures and recovered after successes"
        })

    def _print_summary(self):
        """Print test summary"""

        print("\n" + "="*50)
        print("📋 TEST RESULTS SUMMARY")
        print("="*50)

        for result in self.test_results:
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"\n{status}: {result['test']}")
            print(f"  {result['details']}")

        passed = sum(1 for r in self.test_results if r["passed"])
        total = len(self.test_results)

        print(f"\n{'='*50}")
        print(f"Overall: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
        print("="*50)


def validate_optimizations():
    """Validate all optimizations are working"""
    from agent_factory import create_optimized_system

    orchestrator = create_optimized_system()
    test_suite = PerformanceTestSuite(orchestrator)
    test_suite.run_all_tests()


if __name__ == "__main__":
    validate_optimizations()