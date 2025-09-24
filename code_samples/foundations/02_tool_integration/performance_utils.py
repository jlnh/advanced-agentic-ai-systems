"""
Performance Optimization Utilities - Caching and batch operations
"""

import functools
import time
from typing import List, Dict, Any

# Tool priority configuration
TOOL_PRIORITIES = {
    "file_operations": 1,    # Fastest, free
    "wikipedia": 2,          # Fast, free
    "web_search": 3,         # Moderate speed, free
    "custom_api": 4          # Varies by API
}

@functools.lru_cache(maxsize=100)
def cached_web_search(query: str) -> str:
    """Cache search results to avoid repeated API calls"""
    # Note: In real implementation, would call actual search tool
    # This is a placeholder for demonstration
    return f"Cached result for: {query}"

def batch_file_operations(files_to_read: List[str], read_tool) -> Dict[str, str]:
    """Read multiple files in one operation instead of separate calls"""
    file_contents = {}
    for filename in files_to_read:
        try:
            content = read_tool.run(filename)
            file_contents[filename] = content
        except Exception as e:
            file_contents[filename] = f"Error: {e}"
    return file_contents

def robust_multi_tool_execution(steps: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Execute multiple tool steps with error recovery"""
    results = {}
    for i, step in enumerate(steps):
        try:
            # In real implementation, would execute the actual step
            result = f"Step {i} executed successfully"
            results[f"step_{i}"] = result
        except Exception as e:
            print(f"Step {i} failed: {e}")
            # Decide whether to continue or abort
            if step.get("is_critical", False):
                raise
            results[f"step_{i}"] = f"Skipped due to error: {e}"
    return results

class PerformanceOptimizer:
    """Optimize agent performance through caching and batching"""

    def __init__(self):
        self.cache = {}
        self.batch_queue = []

    def should_cache_result(self, operation_type: str) -> bool:
        """Determine if operation result should be cached"""
        cacheable_operations = ["web_search", "wikipedia", "data_analysis"]
        return operation_type in cacheable_operations

    def get_cached_result(self, key: str) -> Any:
        """Retrieve cached result if available"""
        return self.cache.get(key)

    def cache_result(self, key: str, result: Any) -> None:
        """Store result in cache"""
        self.cache[key] = {
            "result": result,
            "timestamp": time.time()
        }

    def clear_expired_cache(self, max_age_seconds: int = 3600) -> None:
        """Remove cached results older than max_age_seconds"""
        current_time = time.time()
        expired_keys = [
            key for key, value in self.cache.items()
            if current_time - value["timestamp"] > max_age_seconds
        ]
        for key in expired_keys:
            del self.cache[key]