"""
Utility functions for optimization including adaptive optimizer,
intelligent batcher, and dynamic model selector.
"""

import os
import time
import threading
import random
from concurrent.futures import ThreadPoolExecutor, Future
from queue import Queue
from typing import List, Dict, Any, Callable
from dotenv import load_dotenv

from optimized_orchestrator import OptimizedOrchestrator
from task_models import Task

# Load environment variables
load_dotenv()


class AdaptiveOptimizer:
    """
    Self-tuning optimizer that learns from execution patterns
    and automatically adjusts parameters for better performance.
    """

    def __init__(self, orchestrator: OptimizedOrchestrator):
        self.orchestrator = orchestrator
        self.execution_history = []
        self.performance_model = {}
        self.optimization_rules = self._initialize_rules()

    def _initialize_rules(self) -> List[Dict]:
        """Define optimization rules based on patterns"""
        return [
            {
                "condition": lambda m: m["error_rate"] > 0.1,
                "action": "increase_retries",
                "params": {"max_retries": 4}
            },
            {
                "condition": lambda m: m["cache_hit_rate"] < 0.2,
                "action": "optimize_caching",
                "params": {"cache_size": 200}
            },
            {
                "condition": lambda m: m["parallel_speedup"] < 1.5,
                "action": "increase_parallelism",
                "params": {"max_workers": 5}
            },
            {
                "condition": lambda m: m["total_cost"] > 0.4,
                "action": "reduce_costs",
                "params": {"model": "gpt-3.5-turbo", "max_tokens": 300}
            }
        ]

    def analyze_and_optimize(self, metrics: Dict):
        """Analyze metrics and apply optimizations"""

        self.execution_history.append(metrics)

        # Apply matching rules
        for rule in self.optimization_rules:
            if rule["condition"](metrics):
                print(f"🔧 Applying optimization: {rule['action']}")
                self._apply_optimization(rule["action"], rule["params"])

    def _apply_optimization(self, action: str, params: Dict):
        """Apply specific optimization to orchestrator"""

        if action == "increase_retries":
            self.orchestrator.max_retries = params["max_retries"]

        elif action == "optimize_caching":
            if self.orchestrator.result_cache:
                self.orchestrator.result_cache.max_size = params["cache_size"]

        elif action == "increase_parallelism":
            # Recreate executor with more workers
            self.orchestrator.executor.shutdown(wait=False)
            self.orchestrator.executor = ThreadPoolExecutor(
                max_workers=params["max_workers"]
            )

        elif action == "reduce_costs":
            # Apply cost reduction parameters
            for agent in self.orchestrator.agents.values():
                if hasattr(agent, 'llm'):
                    agent.llm.model_name = params["model"]
                    agent.llm.max_tokens = params["max_tokens"]

    def predict_optimal_strategy(self, task_count: int) -> str:
        """Predict best execution strategy based on task count"""

        if task_count <= 2:
            return "sequential"  # Overhead not worth it
        elif task_count <= 5:
            return "parallel"    # Simple parallel execution
        else:
            return "hybrid"      # Complex dependency management


class IntelligentBatcher:
    """
    Batch similar requests to reduce API calls and costs.
    Can reduce costs by 50% for batch workloads.
    """

    def __init__(self, batch_size: int = 5, wait_time: float = 1.0):
        self.batch_size = batch_size
        self.wait_time = wait_time
        self.pending_tasks = []
        self.task_queue = Queue()
        self.results = {}
        self.processing = False

    def add_task(self, task: Task) -> Future:
        """Add task to batch queue"""
        future = Future()
        self.task_queue.put((task, future))

        if not self.processing:
            # Start batch processor
            threading.Thread(target=self._process_batches).start()
            self.processing = True

        return future

    def _process_batches(self):
        """Process tasks in batches"""

        while True:
            batch = []
            futures = []

            # Collect batch
            deadline = time.time() + self.wait_time
            while len(batch) < self.batch_size and time.time() < deadline:
                try:
                    remaining = deadline - time.time()
                    task, future = self.task_queue.get(timeout=max(0.1, remaining))
                    batch.append(task)
                    futures.append(future)
                except:
                    break  # Timeout or empty queue

            if not batch:
                self.processing = False
                break

            # Process batch
            print(f"🎯 Processing batch of {len(batch)} tasks")
            results = self._execute_batch(batch)

            # Set futures
            for future, result in zip(futures, results):
                future.set_result(result)

    def _execute_batch(self, tasks: List[Task]) -> List[Dict]:
        """Execute batch of tasks efficiently"""

        # Group by agent type for even better batching
        tasks_by_agent = {}
        for task in tasks:
            if task.agent_type not in tasks_by_agent:
                tasks_by_agent[task.agent_type] = []
            tasks_by_agent[task.agent_type].append(task)

        results = []
        for agent_type, agent_tasks in tasks_by_agent.items():
            # Combine prompts for batch execution
            combined_prompt = "\n\n---\n\n".join([
                f"Task {i+1}: {t.description}"
                for i, t in enumerate(agent_tasks)
            ])

            # Single API call for multiple tasks
            batch_result = self._execute_combined(agent_type, combined_prompt)

            # Split results
            split_results = self._split_batch_results(batch_result, len(agent_tasks))
            results.extend(split_results)

        return results

    def _execute_combined(self, agent_type: str, combined_prompt: str) -> str:
        """Execute combined prompt with single API call"""
        # Implementation depends on your agent setup
        return f"Combined results for {agent_type}"

    def _split_batch_results(self, combined_result: str, count: int) -> List[Dict]:
        """Split combined result into individual task results"""
        # Simple splitting - in production, use markers or parsing
        parts = combined_result.split("---")[:count]
        return [{"success": True, "output": part} for part in parts]


class DynamicModelSelector:
    """
    Automatically selects the most cost-effective model
    based on task complexity and requirements.
    """

    def __init__(self):
        self.models = {
            "gpt-3.5-turbo": {"cost": 0.002, "quality": 0.7, "speed": 0.9},
            "gpt-4": {"cost": 0.03, "quality": 0.95, "speed": 0.6},
            "gpt-4-turbo": {"cost": 0.01, "quality": 0.9, "speed": 0.8}
        }
        self.task_patterns = self._load_patterns()

    def _load_patterns(self) -> Dict:
        """Load task complexity patterns"""
        return {
            "simple": ["find", "list", "search", "get"],
            "moderate": ["analyze", "compare", "summarize"],
            "complex": ["create", "design", "strategize", "evaluate"]
        }

    def select_model(self, task: Task, budget_remaining: float) -> str:
        """Select optimal model for task"""

        # Determine task complexity
        complexity = self._assess_complexity(task.description)

        # Filter models by budget
        affordable_models = [
            model for model, specs in self.models.items()
            if specs["cost"] <= budget_remaining
        ]

        if not affordable_models:
            return "gpt-3.5-turbo"  # Fallback to cheapest

        # Score models based on task needs
        if complexity == "simple":
            # Prioritize speed and cost
            return min(affordable_models,
                      key=lambda m: self.models[m]["cost"])

        elif complexity == "complex":
            # Prioritize quality
            return max(affordable_models,
                      key=lambda m: self.models[m]["quality"])

        else:
            # Balance all factors
            return self._balanced_selection(affordable_models)

    def _assess_complexity(self, description: str) -> str:
        """Assess task complexity from description"""

        description_lower = description.lower()

        for complexity, patterns in self.task_patterns.items():
            if any(pattern in description_lower for pattern in patterns):
                if complexity == "simple":
                    return "simple"
                elif complexity == "complex":
                    return "complex"

        return "moderate"

    def _balanced_selection(self, models: List[str]) -> str:
        """Select model with best overall value"""

        scores = {}
        for model in models:
            specs = self.models[model]
            # Value = quality * speed / cost
            scores[model] = (specs["quality"] * specs["speed"]) / specs["cost"]

        return max(scores, key=scores.get)


def calculate_optimal_workers(task_count: int, avg_task_duration: float) -> int:
    """
    Calculate optimal number of workers based on workload.
    Too many workers = API rate limit issues
    Too few workers = underutilized resources
    """

    # Consider API rate limits (typically 50-100 req/min)
    max_by_rate_limit = 5

    # Consider task characteristics
    if avg_task_duration < 5:  # Quick tasks
        optimal = min(3, task_count)
    elif avg_task_duration < 15:  # Medium tasks
        optimal = min(5, task_count // 2)
    else:  # Long tasks
        optimal = min(10, task_count // 3)

    return min(optimal, max_by_rate_limit)


def smart_retry(func: Callable, max_retries: int = 3):
    """Intelligent retry with exponential backoff and jitter"""

    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "rate limit" in str(e).lower():
                # Longer wait for rate limits
                time.sleep(60)
            elif "timeout" in str(e).lower():
                # Short wait with jitter
                time.sleep(2**attempt + random.random())
            else:
                if attempt == max_retries - 1:
                    raise