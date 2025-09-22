# src/agentic_ai/core/memory/semantic_cache.py
import hashlib
import json
import time
from typing import Optional, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from langchain.embeddings import OpenAIEmbeddings
import os

class SemanticCache:
    """In-memory semantic cache for development (use Redis in production)"""
    
    def __init__(self, similarity_threshold=0.85, ttl_seconds=3600, max_cache_size=1000):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.similarity_threshold = similarity_threshold
        self.ttl_seconds = ttl_seconds
        self.max_cache_size = max_cache_size
        
        # In-memory storage (use Redis in production)
        self.cache = {}
        self.embedding_cache = {}
        self.access_times = {}
        
    def generate_cache_key(self, query: str, context: Dict = None) -> str:
        """Create unique key including optional context"""
        cache_input = {
            "query": query,
            "context": context or {}
        }
        
        return hashlib.sha256(
            json.dumps(cache_input, sort_keys=True).encode()
        ).hexdigest()[:16]
    
    def get(self, query: str, context: Dict = None) -> Optional[Dict]:
        """Get cached result for query"""
        # Try exact match first
        cache_key = self.generate_cache_key(query, context)
        if cache_key in self.cache:
            cached_item = self.cache[cache_key]
            if time.time() - cached_item["timestamp"] < self.ttl_seconds:
                self.access_times[cache_key] = time.time()
                return cached_item["result"]
            else:
                # Expired
                del self.cache[cache_key]
                if cache_key in self.embedding_cache:
                    del self.embedding_cache[cache_key]
        
        # Try semantic similarity
        similar_result = self.find_similar_query(query)
        if similar_result:
            return similar_result["result"]
        
        return None
    
    def put(self, query: str, result: Dict, context: Dict = None):
        """Store result in cache"""
        cache_key = self.generate_cache_key(query, context)
        
        # Evict oldest if at capacity
        if len(self.cache) >= self.max_cache_size:
            oldest_key = min(self.access_times, key=self.access_times.get)
            del self.cache[oldest_key]
            if oldest_key in self.embedding_cache:
                del self.embedding_cache[oldest_key]
            del self.access_times[oldest_key]
        
        # Store result and embedding
        self.cache[cache_key] = {
            "query": query,
            "result": result,
            "timestamp": time.time()
        }
        
        # Store embedding for similarity search
        try:
            query_embedding = self.embeddings.embed_query(query)
            self.embedding_cache[cache_key] = query_embedding
        except Exception as e:
            print(f"⚠️ Failed to generate embedding: {e}")
        
        self.access_times[cache_key] = time.time()
    
    def find_similar_query(self, query: str) -> Optional[Dict]:
        """Find semantically similar cached query"""
        if not self.embedding_cache:
            return None
        
        try:
            query_embedding = self.embeddings.embed_query(query)
            
            best_match = None
            best_score = 0
            
            for cache_key, cached_embedding in self.embedding_cache.items():
                similarity = cosine_similarity(
                    [query_embedding], 
                    [cached_embedding]
                )[0][0]
                
                if similarity > self.similarity_threshold and similarity > best_score:
                    if cache_key in self.cache:  # Still valid
                        cached_item = self.cache[cache_key]
                        if time.time() - cached_item["timestamp"] < self.ttl_seconds:
                            best_score = similarity
                            best_match = {
                                "result": cached_item["result"],
                                "similarity": similarity,
                                "original_query": cached_item["query"]
                            }
            
            return best_match
            
        except Exception as e:
            print(f"⚠️ Error in similarity search: {e}")
            return None