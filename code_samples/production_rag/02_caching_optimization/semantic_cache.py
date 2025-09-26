import hashlib
import json
import time
from typing import Optional, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import redis
from langchain_compat import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class SemanticCache:
    """Production-grade semantic cache with similarity matching"""

    def __init__(self,
                 similarity_threshold=0.85,
                 ttl_seconds=3600,
                 max_cache_size=10000):

        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small"  # Cheap but effective
        )

        # Redis for distributed caching in production
        # Note: maxmemory and maxmemory_policy are Redis server config, not client config
        try:
            self.redis_client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", "6379")),
                password=os.getenv("REDIS_PASSWORD", None),
                db=int(os.getenv("REDIS_DB", "0")),
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            self.redis_available = True
            print("✓ Redis connection established")
        except redis.ConnectionError:
            print("⚠ Redis not available, using in-memory cache fallback")
            self.redis_client = None
            self.redis_available = False
            # Fallback to in-memory storage
            self.memory_cache = {}

        self.similarity_threshold = similarity_threshold
        self.ttl_seconds = ttl_seconds

        # Local embedding cache for fast similarity checks
        self.embedding_cache = {}

    def generate_cache_key(self, query: str, context: Dict = None) -> str:
        """Create unique key including optional context"""

        cache_input = {
            "query": query,
            "context": context or {}
        }

        # Stable hash for exact matches
        return hashlib.sha256(
            json.dumps(cache_input, sort_keys=True).encode()
        ).hexdigest()[:16]

    def find_similar_query(self, query: str) -> Optional[Dict]:
        """Find semantically similar cached query"""

        # Generate embedding for incoming query
        query_embedding = self.embeddings.embed_query(query)

        if self.redis_available:
            # Get all cached embeddings from Redis
            cached_keys = self.redis_client.keys("cache:embedding:*")

            if not cached_keys:
                return None

            best_match = None
            best_score = 0

            for key in cached_keys:
                # Retrieve cached embedding
                cached_data = self.redis_client.hgetall(key)
                cached_embedding = json.loads(cached_data.get("embedding", "[]"))

                if not cached_embedding:
                    continue

                # Calculate similarity
                similarity = cosine_similarity(
                    [query_embedding],
                    [cached_embedding]
                )[0][0]

                if similarity > self.similarity_threshold and similarity > best_score:
                    best_score = similarity
                    best_match = {
                        "key": cached_data.get("response_key"),
                        "original_query": cached_data.get("query"),
                        "similarity": similarity
                    }

            return best_match
        else:
            # Fallback to in-memory cache
            if not hasattr(self, 'memory_cache') or not self.memory_cache:
                return None

            best_match = None
            best_score = 0

            for cache_key, cached_data in self.memory_cache.items():
                if not cache_key.startswith("embedding:"):
                    continue

                cached_embedding = cached_data.get("embedding", [])
                if not cached_embedding:
                    continue

                # Calculate similarity
                similarity = cosine_similarity(
                    [query_embedding],
                    [cached_embedding]
                )[0][0]

                if similarity > self.similarity_threshold and similarity > best_score:
                    best_score = similarity
                    best_match = {
                        "key": cached_data.get("response_key"),
                        "original_query": cached_data.get("query"),
                        "similarity": similarity
                    }

            return best_match

    def cache_result(self, query: str, result: Dict, cost: float):
        """Cache query result with embedding"""

        # Generate cache keys
        cache_key = self.generate_cache_key(query)
        embedding_key = f"cache:embedding:{cache_key}"
        response_key = f"cache:response:{cache_key}"

        # Generate embedding
        query_embedding = self.embeddings.embed_query(query)

        # Store embedding with metadata
        embedding_data = {
            "embedding": json.dumps(query_embedding) if self.redis_available else query_embedding,
            "query": query,
            "response_key": cache_key,
            "cost": cost,
            "timestamp": time.time()
        }

        if self.redis_available:
            # Store in Redis with TTL
            self.redis_client.hmset(embedding_key, embedding_data)
            self.redis_client.expire(embedding_key, self.ttl_seconds)

            # Store response
            self.redis_client.set(response_key, json.dumps(result), ex=self.ttl_seconds)
        else:
            # Store in memory cache
            if not hasattr(self, 'memory_cache'):
                self.memory_cache = {}

            self.memory_cache[f"embedding:{cache_key}"] = embedding_data
            self.memory_cache[f"response:{cache_key}"] = result

        return cache_key

    def get_cached_response(self, response_key: str) -> Optional[Dict]:
        """Retrieve cached response by key"""
        if self.redis_available:
            cached_response = self.redis_client.get(f"cache:response:{response_key}")
            if cached_response:
                return json.loads(cached_response)
        else:
            # Check memory cache
            if hasattr(self, 'memory_cache'):
                return self.memory_cache.get(f"response:{response_key}")
        return None


if __name__ == "__main__":
    # Example usage
    cache = SemanticCache()

    # Example queries
    queries = [
        "What's the weather in San Francisco?",
        "Tell me the SF weather",
        "How's the weather in San Francisco today?"
    ]

    print("Testing semantic cache similarity...")
    for i, query in enumerate(queries):
        print(f"\nQuery {i+1}: {query}")
        similar = cache.find_similar_query(query)
        if similar:
            print(f"Found similar: {similar['original_query']} (similarity: {similar['similarity']:.3f})")
        else:
            print("No similar query found")