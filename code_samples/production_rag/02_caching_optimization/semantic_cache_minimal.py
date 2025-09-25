import hashlib
import json
import time
from typing import Optional, Dict, Any
import redis
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class MinimalSemanticCache:
    """Minimal semantic cache that works without OpenAI embeddings for testing"""

    def __init__(self,
                 similarity_threshold=0.5,  # Lower threshold for simple similarity
                 ttl_seconds=3600,
                 max_cache_size=10000):

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
        except (redis.ConnectionError, redis.exceptions.ConnectionError):
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

    def simple_similarity(self, query1: str, query2: str) -> float:
        """Simple similarity calculation based on word overlap and common patterns"""
        words1 = set(word.lower().strip('?.,!') for word in query1.split())
        words2 = set(word.lower().strip('?.,!') for word in query2.split())

        # Remove common stop words for better matching
        stop_words = {'the', 'is', 'in', 'on', 'at', 'to', 'a', 'an', 'and', 'or', 'but', 'what', 'how', 'tell', 'me'}
        words1 = words1 - stop_words
        words2 = words2 - stop_words

        if not words1 or not words2:
            return 0.0

        # Check for key concept matches
        key_concepts = {
            'weather': ['weather', 'climate', 'temperature', 'sunny', 'cloudy', 'rain'],
            'location': ['sf', 'san francisco', 'nyc', 'new york', 'city'],
            'money': ['tip', 'calculate', 'percent', '%', 'dollar', '$'],
        }

        concept_matches = 0
        for concept, terms in key_concepts.items():
            if any(term in ' '.join(words1) for term in terms) and any(term in ' '.join(words2) for term in terms):
                concept_matches += 1

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        # Jaccard similarity
        jaccard = intersection / union if union > 0 else 0.0

        # Boost for similar structure/length
        length_factor = min(len(query1), len(query2)) / max(len(query1), len(query2))

        # Concept bonus
        concept_bonus = concept_matches * 0.3

        return min(1.0, jaccard * 0.5 + length_factor * 0.2 + concept_bonus)

    def find_similar_query(self, query: str) -> Optional[Dict]:
        """Find semantically similar cached query using simple similarity"""

        if self.redis_available:
            # Get all cached queries from Redis
            cached_keys = self.redis_client.keys("cache:query:*")

            if not cached_keys:
                return None

            best_match = None
            best_score = 0

            for key in cached_keys:
                # Retrieve cached query data
                cached_data = self.redis_client.hgetall(key)
                cached_query = cached_data.get("query", "")

                if not cached_query:
                    continue

                # Calculate similarity
                similarity = self.simple_similarity(query, cached_query)

                if similarity > self.similarity_threshold and similarity > best_score:
                    best_score = similarity
                    best_match = {
                        "key": cached_data.get("response_key"),
                        "original_query": cached_query,
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
                if not cache_key.startswith("query:"):
                    continue

                cached_query = cached_data.get("query", "")
                if not cached_query:
                    continue

                # Calculate similarity
                similarity = self.simple_similarity(query, cached_query)

                if similarity > self.similarity_threshold and similarity > best_score:
                    best_score = similarity
                    best_match = {
                        "key": cached_data.get("response_key"),
                        "original_query": cached_query,
                        "similarity": similarity
                    }

            return best_match

    def cache_result(self, query: str, result: Dict, cost: float):
        """Cache query result"""

        # Generate cache keys
        cache_key = self.generate_cache_key(query)
        query_key = f"cache:query:{cache_key}"
        response_key = f"cache:response:{cache_key}"

        # Store query with metadata
        query_data = {
            "query": query,
            "response_key": cache_key,
            "cost": cost,
            "timestamp": time.time()
        }

        if self.redis_available:
            # Store in Redis with TTL
            self.redis_client.hset(query_key, mapping=query_data)
            self.redis_client.expire(query_key, self.ttl_seconds)

            # Store response
            self.redis_client.set(response_key, json.dumps(result), ex=self.ttl_seconds)
        else:
            # Store in memory cache
            if not hasattr(self, 'memory_cache'):
                self.memory_cache = {}

            self.memory_cache[f"query:{cache_key}"] = query_data
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

    def clear_cache(self):
        """Clear all cached data"""
        if self.redis_available:
            # Delete all cache keys
            keys = self.redis_client.keys("cache:*")
            if keys:
                self.redis_client.delete(*keys)
        else:
            if hasattr(self, 'memory_cache'):
                self.memory_cache.clear()

    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        if self.redis_available:
            query_keys = self.redis_client.keys("cache:query:*")
            response_keys = self.redis_client.keys("cache:response:*")
            return {
                "cache_type": "Redis",
                "query_count": len(query_keys),
                "response_count": len(response_keys),
                "redis_available": True
            }
        else:
            if hasattr(self, 'memory_cache'):
                query_count = sum(1 for k in self.memory_cache.keys() if k.startswith("query:"))
                response_count = sum(1 for k in self.memory_cache.keys() if k.startswith("response:"))
                return {
                    "cache_type": "Memory",
                    "query_count": query_count,
                    "response_count": response_count,
                    "redis_available": False
                }
            return {"cache_type": "None", "query_count": 0, "response_count": 0, "redis_available": False}


if __name__ == "__main__":
    # Example usage
    print("Minimal Semantic Cache Test")
    print("=" * 40)

    cache = MinimalSemanticCache()

    # Test caching and retrieval
    test_data = [
        ("What's the weather in San Francisco?", {"answer": "Sunny, 72°F"}),
        ("How is the weather in NYC?", {"answer": "Cloudy, 65°F"}),
        ("Calculate 15% tip on $50", {"answer": "$7.50"}),
    ]

    # Cache some results
    print("Caching test queries...")
    for query, result in test_data:
        cache.cache_result(query, result, 0.05)
        print(f"✓ Cached: {query[:30]}...")

    # Test similar queries
    print(f"\nTesting similarity detection...")
    test_queries = [
        "What's the weather in SF?",  # Similar to first
        "Tell me the SF weather",     # Similar to first
        "How's the weather in New York?",  # Similar to second
        "What's 15% tip for $50?",    # Similar to third
        "What time is it?",           # Not similar to any
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        similar = cache.find_similar_query(query)
        if similar:
            print(f"  ✓ Found similar: '{similar['original_query']}'")
            print(f"  ✓ Similarity: {similar['similarity']:.3f}")

            # Try to get the cached response
            response = cache.get_cached_response(similar['key'])
            if response:
                print(f"  ✓ Cached response: {response}")
            else:
                print("  ✗ Could not retrieve cached response")
        else:
            print("  ✗ No similar query found (cache miss)")

    # Show cache statistics
    print(f"\nCache Statistics:")
    stats = cache.get_cache_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")