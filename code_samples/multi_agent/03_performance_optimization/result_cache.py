"""
LRU cache implementation for agent results to avoid redundant API calls.
Can reduce costs by 40%+ for repetitive queries.
"""

import time
import threading
import hashlib
from typing import Optional, Dict
from task_models import Task


class ResultCache:
    """
    LRU cache for agent results to avoid redundant API calls.
    Can reduce costs by 40%+ for repetitive queries.
    """

    def __init__(self, max_size: int = 100, ttl: int = 3600):
        self.max_size = max_size
        self.ttl = ttl  # Time to live in seconds
        self.cache = {}
        self.timestamps = {}
        self.access_count = {}
        self.lock = threading.Lock()

    def _generate_key(self, task: Task) -> str:
        """Generate cache key from task"""
        key_parts = [
            task.agent_type,
            task.description,
            str(sorted(task.dependencies))
        ]
        key_string = "|".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()

    def get(self, task: Task) -> Optional[Dict]:
        """Retrieve cached result if available and valid"""
        with self.lock:
            key = self._generate_key(task)

            if key not in self.cache:
                return None

            # Check if cache entry has expired
            if time.time() - self.timestamps[key] > self.ttl:
                del self.cache[key]
                del self.timestamps[key]
                del self.access_count[key]
                return None

            # Update access count for LRU
            self.access_count[key] = time.time()
            return self.cache[key]

    def put(self, task: Task, result: Dict):
        """Store result in cache"""
        with self.lock:
            key = self._generate_key(task)

            # Evict least recently used if at capacity
            if len(self.cache) >= self.max_size:
                lru_key = min(self.access_count, key=self.access_count.get)
                del self.cache[lru_key]
                del self.timestamps[lru_key]
                del self.access_count[lru_key]

            self.cache[key] = result
            self.timestamps[key] = time.time()
            self.access_count[key] = time.time()