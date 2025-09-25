"""
Performance monitoring and metrics collection for multi-agent systems.
"""

import time
from typing import Dict
from dataclasses import dataclass


class PerformanceMetrics:
    """Track detailed performance metrics"""

    def __init__(self):
        self.start_time = time.time()
        self.task_timings = {}
        self.token_usage = {}
        self.costs = {}
        self.errors = []
        self.cache_hits = 0
        self.cache_misses = 0

    def record_task(self, task_id: str, duration: float, tokens: int, cost: float):
        self.task_timings[task_id] = duration
        self.token_usage[task_id] = tokens
        self.costs[task_id] = cost

    def get_summary(self) -> Dict:
        total_time = time.time() - self.start_time
        return {
            "total_duration": total_time,
            "parallel_speedup": self._calculate_speedup(),
            "total_tokens": sum(self.token_usage.values()),
            "total_cost": sum(self.costs.values()),
            "cache_hit_rate": self.cache_hits / (self.cache_hits + self.cache_misses) if self.cache_misses > 0 else 1.0,
            "error_rate": len(self.errors) / len(self.task_timings) if self.task_timings else 0
        }

    def _calculate_speedup(self) -> float:
        """Calculate parallel speedup vs sequential execution"""
        if not self.task_timings:
            return 1.0
        sequential_time = sum(self.task_timings.values())
        parallel_time = time.time() - self.start_time
        return sequential_time / parallel_time if parallel_time > 0 else 1.0