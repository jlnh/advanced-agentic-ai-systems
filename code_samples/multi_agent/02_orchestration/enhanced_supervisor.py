"""
Enhanced Supervisor Agent with Monitoring and Optimization
Extended supervisor with performance tracking, optimization, and cost management.
"""

from supervisor_agent import SupervisorAgent, ExecutionPlan, Task, TaskType
from typing import Dict, Any, List
from langchain.agents import AgentExecutor
import time
import hashlib
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EnhancedSupervisor(SupervisorAgent):
    """Extended supervisor with monitoring and optimization"""

    def __init__(self, specialized_agents: Dict[str, AgentExecutor]):
        super().__init__(specialized_agents)
        self.performance_metrics = {}
        self.optimization_enabled = True
        self.plan_cache = {}
        self.execution_trace = []
        self.metrics = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "total_duration": 0,
            "total_cost": 0
        }
        self.alert_thresholds = {
            "failure_rate": 0.2,  # Alert if >20% failures
            "avg_duration": 60,    # Alert if >60s average
            "cost_per_request": 1.0  # Alert if >$1 per request
        }
        self.budget_per_request = 0.50
        self.cost_tracker = {}

    def monitor_performance(self, task_id: str, metrics: Dict):
        """Track performance metrics for optimization"""

        if task_id not in self.performance_metrics:
            self.performance_metrics[task_id] = []

        self.performance_metrics[task_id].append({
            "timestamp": time.time(),
            "duration": metrics.get("duration", 0),
            "tokens": metrics.get("tokens", 0),
            "cost": metrics.get("cost", 0),
            "success": metrics.get("success", True)
        })

    def optimize_plan(self, plan: ExecutionPlan) -> ExecutionPlan:
        """Optimize execution plan based on historical performance"""

        if not self.optimization_enabled:
            return plan

        # Analyze historical performance
        for task in plan.tasks:
            task_type = task.get("agent_type")

            # Adjust timeout based on historical data
            if task_type in self.performance_metrics:
                avg_duration = self._calculate_average_duration(task_type)
                task["timeout"] = int(avg_duration * 1.5)  # 50% buffer

            # Reorder tasks by historical success rate
            success_rate = self._calculate_success_rate(task_type)
            task["priority"] = int(success_rate * 10)

        # Sort tasks by priority while respecting dependencies
        plan.tasks = self._topological_sort_with_priority(plan.tasks)

        return plan

    def analyze_request(self, request: str) -> ExecutionPlan:
        """Analyze request with caching"""
        # Cache similar request plans
        request_hash = hashlib.md5(request.encode()).hexdigest()

        if request_hash in self.plan_cache:
            print("📦 Using cached execution plan")
            return self.plan_cache[request_hash]

        plan = super().analyze_request(request)
        self.plan_cache[request_hash] = plan
        return plan

    def run(self, request: str) -> Dict[str, Any]:
        """Run with monitoring and alerts"""
        self.metrics["total_requests"] += 1
        start_time = time.time()

        self.trace_event("request_started", {"request": request[:100]})

        try:
            result = super().run(request)
            self.metrics["successful_requests"] += 1
            self.trace_event("request_completed", {"status": result["status"]})
            self.check_alerts()
            return result
        except Exception as e:
            self.metrics["failed_requests"] += 1
            self.trace_event("request_failed", {"error": str(e)})
            self.check_alerts()
            raise
        finally:
            duration = time.time() - start_time
            self.metrics["total_duration"] += duration

    def execute_plan(self, plan: ExecutionPlan) -> Dict[str, Any]:
        """Execute with cost tracking and limits"""
        current_cost = 0.0

        # Estimate costs before execution
        estimated_cost = self.estimate_plan_cost(plan)
        if estimated_cost > self.budget_per_request:
            # Optimize plan to reduce costs
            plan = self.optimize_plan_for_cost(plan)

        # Track actual costs during execution
        original_execute = self._execute_single_task

        def tracked_execute(agent, task, context):
            # Simplified cost tracking - in production use langchain callbacks
            start_time = time.time()
            try:
                result = original_execute(agent, task, context)
                duration = time.time() - start_time

                # Rough cost estimation (replace with actual callback)
                estimated_cost = duration * 0.01  # $0.01 per second rough estimate
                self.cost_tracker[task.id] = estimated_cost
                nonlocal current_cost
                current_cost += estimated_cost

                # Stop if exceeding budget
                if current_cost > self.budget_per_request:
                    raise Exception(f"Cost limit exceeded: ${current_cost:.2f}")

                return result
            except Exception as e:
                self.trace_event("task_failed", {"task_id": task.id, "error": str(e)})
                raise

        self._execute_single_task = tracked_execute

        try:
            result = super().execute_plan(plan)
            print(f"💰 Total cost: ${current_cost:.3f}")
            return result
        finally:
            self._execute_single_task = original_execute

    def trace_event(self, event_type: str, data: Dict):
        """Add event to execution trace"""
        self.execution_trace.append({
            "timestamp": time.time(),
            "type": event_type,
            "data": data
        })

    def get_trace_summary(self):
        """Get human-readable trace summary"""
        summary = []
        for event in self.execution_trace:
            time_str = datetime.fromtimestamp(event["timestamp"]).strftime("%H:%M:%S")
            summary.append(f"[{time_str}] {event['type']}: {event['data'].get('task_id', 'N/A')}")
        return "\n".join(summary)

    def check_alerts(self):
        """Check if any metrics exceed thresholds"""
        if self.metrics["total_requests"] == 0:
            return

        failure_rate = self.metrics["failed_requests"] / self.metrics["total_requests"]
        avg_duration = self.metrics["total_duration"] / self.metrics["total_requests"]

        if failure_rate > self.alert_thresholds["failure_rate"]:
            self.send_alert(f"High failure rate: {failure_rate:.1%}")

        if avg_duration > self.alert_thresholds["avg_duration"]:
            self.send_alert(f"High average duration: {avg_duration:.1f}s")

    def send_alert(self, message: str):
        """Send alert to monitoring system"""
        print(f"🚨 ALERT: {message}")
        # In production: send to PagerDuty, Slack, etc.
        logging.warning(f"ORCHESTRATION_ALERT: {message}")

    def optimize_plan_for_cost(self, plan: ExecutionPlan) -> ExecutionPlan:
        """Optimize plan to reduce costs"""
        # Use cheaper models for simple tasks
        for task in plan.tasks:
            if task["agent_type"] == "research":
                task["model"] = "gpt-3.5-turbo"  # Cheaper model

            # Reduce max tokens for non-critical tasks
            if task.get("priority", 1) > 2:
                task["max_tokens"] = 500

        return plan

    def estimate_plan_cost(self, plan: ExecutionPlan) -> float:
        """Estimate cost before execution"""
        # Rough estimation: $0.10 per task average
        return len(plan.tasks) * 0.10

    def execute_with_fallback(self, request: str) -> Dict:
        """Execute with multiple fallback strategies"""

        try:
            # Try primary execution
            return self.run(request)
        except Exception as primary_error:
            print(f"⚠️ Primary execution failed: {primary_error}")

            # Fallback 1: Simplified sequential execution
            try:
                simple_plan = ExecutionPlan(
                    tasks=[{"id": "simple", "description": request,
                           "agent_type": "research", "dependencies": []}],
                    strategy="sequential",
                    estimated_time=30
                )
                return self.execute_plan(simple_plan)
            except Exception as fallback_error:
                print(f"⚠️ Fallback failed: {fallback_error}")

                # Fallback 2: Direct agent execution
                return self._emergency_direct_execution(request)

    def _emergency_direct_execution(self, request: str) -> Dict:
        """Emergency fallback to single agent"""
        agent = self.agents.get("researcher")
        result = agent.invoke({"input": request})
        return {
            "status": "emergency",
            "output": result.get("output", "Failed to process request"),
            "task_results": {},
            "success_rate": 0.5
        }

    def _calculate_average_duration(self, task_type: str) -> float:
        """Calculate average duration for task type"""
        all_durations = []
        for metrics_list in self.performance_metrics.values():
            for metric in metrics_list:
                all_durations.append(metric["duration"])

        return sum(all_durations) / len(all_durations) if all_durations else 30

    def _calculate_success_rate(self, task_type: str) -> float:
        """Calculate success rate for task type"""
        successes = 0
        total = 0

        for metrics_list in self.performance_metrics.values():
            for metric in metrics_list:
                total += 1
                if metric["success"]:
                    successes += 1

        return successes / total if total > 0 else 1.0

    def _topological_sort_with_priority(self, tasks: List[Dict]) -> List[Dict]:
        """Sort tasks respecting dependencies and priorities"""
        # Implementation of topological sort with priority consideration
        # This is a simplified version
        return sorted(tasks, key=lambda x: (-x.get("priority", 0), x.get("id")))

    def adaptive_retry(self, task: Task, error: Exception) -> bool:
        """Decide whether to retry based on error type and history"""

        error_type = type(error).__name__

        # Don't retry on certain errors
        non_retryable = ["AuthenticationError", "InvalidRequestError"]
        if error_type in non_retryable:
            return False

        # Check historical success after retry
        retry_success_rate = self._calculate_retry_success_rate(task.agent_type)

        # Retry if historically successful
        return retry_success_rate > 0.5

    def _calculate_retry_success_rate(self, agent_type: str) -> float:
        """Calculate success rate for retries"""
        # Simplified implementation
        return 0.7  # 70% success rate on retries

    def get_performance_summary(self) -> Dict:
        """Get comprehensive performance summary"""
        if self.metrics["total_requests"] == 0:
            return {"message": "No requests processed yet"}

        return {
            "total_requests": self.metrics["total_requests"],
            "success_rate": self.metrics["successful_requests"] / self.metrics["total_requests"],
            "avg_duration": self.metrics["total_duration"] / self.metrics["total_requests"],
            "total_cost": self.metrics["total_cost"],
            "avg_cost_per_request": self.metrics["total_cost"] / self.metrics["total_requests"],
            "cached_plans": len(self.plan_cache),
            "trace_events": len(self.execution_trace)
        }