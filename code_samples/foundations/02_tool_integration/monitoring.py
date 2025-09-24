"""
Tool Usage Monitoring - Track and analyze tool performance
"""

import time
from functools import wraps

class ToolUsageTracker:
    """Track tool usage statistics and performance"""

    def __init__(self):
        self.tool_calls = {}
        self.execution_times = {}

    def track_tool_call(self, tool_name, duration, success):
        """Record a tool call with its performance metrics"""
        if tool_name not in self.tool_calls:
            self.tool_calls[tool_name] = {"count": 0, "successes": 0, "failures": 0}

        self.tool_calls[tool_name]["count"] += 1
        if success:
            self.tool_calls[tool_name]["successes"] += 1
        else:
            self.tool_calls[tool_name]["failures"] += 1

        if tool_name not in self.execution_times:
            self.execution_times[tool_name] = []
        self.execution_times[tool_name].append(duration)

    def print_stats(self):
        """Print comprehensive tool usage statistics"""
        print("\n📊 Tool Usage Statistics:")
        for tool, stats in self.tool_calls.items():
            avg_time = sum(self.execution_times[tool]) / len(self.execution_times[tool])
            success_rate = stats["successes"] / stats["count"] * 100
            print(f"  {tool}: {stats['count']} calls, {success_rate:.1f}% success, {avg_time:.2f}s avg")

def rate_limit(calls_per_minute=10):
    """Decorator to rate limit function calls"""
    def decorator(func):
        last_calls = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove calls older than 1 minute
            last_calls[:] = [call_time for call_time in last_calls if now - call_time < 60]

            if len(last_calls) >= calls_per_minute:
                sleep_time = 60 - (now - last_calls[0])
                time.sleep(sleep_time)

            last_calls.append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator