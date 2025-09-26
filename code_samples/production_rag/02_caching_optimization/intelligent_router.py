from enum import Enum
from typing import List, Tuple, Dict
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class QueryComplexity(Enum):
    SIMPLE = "simple"      # Factual, single-step
    MEDIUM = "medium"      # Multi-step, some reasoning
    COMPLEX = "complex"    # Deep analysis, creativity


class IntelligentRouter:
    """Route queries to appropriate models based on complexity"""

    def __init__(self):
        # Complexity indicators
        self.simple_patterns = [
            "what is", "when is", "where is", "who is",
            "define", "list", "name", "count"
        ]

        self.complex_patterns = [
            "analyze", "compare", "evaluate", "design",
            "create", "explain why", "how would you",
            "develop", "strategy", "comprehensive"
        ]

        # Model configurations with costs
        self.model_configs = {
            QueryComplexity.SIMPLE: {
                "model": "gpt-3.5-turbo",
                "temperature": 0,
                "max_tokens": 500,
                "cost_per_1k": 0.0015
            },
            QueryComplexity.MEDIUM: {
                "model": "gpt-3.5-turbo",
                "temperature": 0.3,
                "max_tokens": 1000,
                "cost_per_1k": 0.0015
            },
            QueryComplexity.COMPLEX: {
                "model": "gpt-4",
                "temperature": 0.7,
                "max_tokens": 2000,
                "cost_per_1k": 0.03
            }
        }

    def analyze_complexity(self, query: str) -> Tuple[QueryComplexity, float]:
        """Determine query complexity with confidence score"""

        query_lower = query.lower()

        # Check for simple patterns
        simple_score = sum(
            1 for pattern in self.simple_patterns
            if pattern in query_lower
        ) * 0.3

        # Check for complex patterns
        complex_score = sum(
            1 for pattern in self.complex_patterns
            if pattern in query_lower
        ) * 0.5

        # Length heuristic (longer = more complex usually)
        length_score = min(len(query.split()) / 50, 1.0) * 0.2

        # Question mark count (multiple questions = complex)
        question_score = query.count('?') * 0.1

        total_score = complex_score - simple_score + length_score + question_score

        if total_score < 0.3:
            return QueryComplexity.SIMPLE, 1 - total_score
        elif total_score < 0.6:
            return QueryComplexity.MEDIUM, 0.7
        else:
            return QueryComplexity.COMPLEX, total_score

    def estimate_cost(self, query: str, config: Dict) -> float:
        """Estimate cost based on query length and model"""
        # Rough estimation: 1 word ≈ 1.3 tokens
        estimated_tokens = len(query.split()) * 1.3 + config["max_tokens"]
        return (estimated_tokens / 1000) * config["cost_per_1k"]

    def route_query(self, query: str) -> Dict:
        """Route to appropriate model configuration"""

        complexity, confidence = self.analyze_complexity(query)
        config = self.model_configs[complexity]

        return {
            "model": config["model"],
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"],
            "complexity": complexity.value,
            "confidence": confidence,
            "estimated_cost": self.estimate_cost(query, config)
        }

    def get_routing_stats(self, queries: List[str]) -> Dict:
        """Analyze routing distribution for a set of queries"""
        stats = {
            QueryComplexity.SIMPLE.value: 0,
            QueryComplexity.MEDIUM.value: 0,
            QueryComplexity.COMPLEX.value: 0
        }

        total_cost = 0
        for query in queries:
            routing = self.route_query(query)
            stats[routing["complexity"]] += 1
            total_cost += routing["estimated_cost"]

        # Calculate percentages
        total_queries = len(queries)
        for key in stats:
            stats[key] = {
                "count": stats[key],
                "percentage": (stats[key] / total_queries) * 100 if total_queries > 0 else 0
            }

        return {
            "distribution": stats,
            "total_estimated_cost": total_cost,
            "average_cost_per_query": total_cost / total_queries if total_queries > 0 else 0
        }


if __name__ == "__main__":
    # Example usage
    router = IntelligentRouter()

    # Test queries of different complexities
    test_queries = [
        "What is the capital of France?",  # Simple
        "List all European countries",  # Simple
        "Compare the economic policies of France and Germany",  # Complex
        "How would you design a recommendation system?",  # Complex
        "Explain the process of photosynthesis",  # Medium
        "What are the benefits of renewable energy?"  # Medium
    ]

    print("Query Routing Analysis:")
    print("=" * 50)

    for query in test_queries:
        routing = router.route_query(query)
        print(f"\nQuery: {query}")
        print(f"Complexity: {routing['complexity']} (confidence: {routing['confidence']:.2f})")
        print(f"Model: {routing['model']}")
        print(f"Estimated cost: ${routing['estimated_cost']:.4f}")

    # Get overall statistics
    stats = router.get_routing_stats(test_queries)
    print(f"\n\nRouting Statistics:")
    print("=" * 30)
    for complexity, data in stats["distribution"].items():
        print(f"{complexity.title()}: {data['count']} queries ({data['percentage']:.1f}%)")
    print(f"Total estimated cost: ${stats['total_estimated_cost']:.4f}")
    print(f"Average cost per query: ${stats['average_cost_per_query']:.4f}")