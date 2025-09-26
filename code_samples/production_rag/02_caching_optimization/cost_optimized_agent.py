import json
import time
import asyncio
from typing import List, Dict
from datetime import datetime
from dotenv import load_dotenv
import os

# Use compatibility layer for LangChain imports
from langchain_compat import (
    ChatOpenAI,
    get_openai_callback,
    create_react_agent,
    AgentExecutor,
    PromptTemplate
)

# Import our custom components
from semantic_cache import SemanticCache
from intelligent_router import IntelligentRouter
from tool_optimizer import ToolOptimizer, Tool, create_sample_tools

# Load environment variables
load_dotenv()


class CostOptimizedAgent:
    """Production agent with all optimization strategies"""

    def __init__(self, tools: List[Tool]):
        self.cache = SemanticCache()
        self.router = IntelligentRouter()
        self.tool_optimizer = ToolOptimizer(tools)

        # Track metrics
        self.metrics = {
            "total_queries": 0,
            "cache_hits": 0,
            "total_cost": 0,
            "total_tokens": 0,
            "cost_saved": 0,
            "query_history": []
        }

        # Simple prompt template for the agent
        self.prompt_template = PromptTemplate(
            input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
            template="""You are a helpful assistant. Use the available tools to answer questions.

Available tools: {tool_names}
{tools}

Question: {input}

{agent_scratchpad}"""
        )

    async def execute(self, query: str, use_cache: bool = True) -> Dict:
        """Execute query with full optimization pipeline"""

        start_time = time.time()
        self.metrics["total_queries"] += 1

        try:
            # Step 1: Check semantic cache
            if use_cache:
                cached_result = self.cache.find_similar_query(query)
                if cached_result:
                    self.metrics["cache_hits"] += 1

                    # Retrieve full response from cache
                    response_key = cached_result["key"]
                    cached_response = self.cache.get_cached_response(response_key)

                    if cached_response:
                        # Track saved cost
                        estimated_saved_cost = 0.05  # Approximate savings
                        self.metrics["cost_saved"] += estimated_saved_cost

                        result = {
                            "response": cached_response,
                            "cached": True,
                            "similarity": cached_result["similarity"],
                            "latency": time.time() - start_time,
                            "cost": 0,
                            "tokens": 0,
                            "original_query": cached_result["original_query"]
                        }

                        self._record_query(query, result)
                        return result

            # Step 2: Route to appropriate model
            routing_config = self.router.route_query(query)

            # Step 3: Select minimal required tools
            selected_tools = self.tool_optimizer.select_tools(query)

            # Step 4: Create optimized agent (simulate execution)
            # Note: In a real implementation, you would use actual LangChain agents
            # For this demo, we'll simulate the response
            simulated_cost = routing_config["estimated_cost"]
            simulated_tokens = int(routing_config["estimated_cost"] * 30000)  # Rough conversion

            # Simulate processing time based on complexity
            if routing_config["complexity"] == "complex":
                await asyncio.sleep(0.1)  # Simulate longer processing
            else:
                await asyncio.sleep(0.05)

            # Create simulated response
            response_content = {
                "answer": f"Processed query: '{query}' using {routing_config['model']}",
                "tools_used": [tool.name for tool in selected_tools],
                "reasoning": f"Query classified as {routing_config['complexity']} complexity"
            }

            # Track metrics
            self.metrics["total_cost"] += simulated_cost
            self.metrics["total_tokens"] += simulated_tokens

            result = {
                "response": response_content,
                "cached": False,
                "model": routing_config["model"],
                "complexity": routing_config["complexity"],
                "confidence": routing_config["confidence"],
                "latency": time.time() - start_time,
                "cost": simulated_cost,
                "tokens": simulated_tokens,
                "tools_selected": len(selected_tools),
                "tools_used": [tool.name for tool in selected_tools]
            }

            # Cache the result if it was expensive
            if use_cache and simulated_cost > 0.01:
                self.cache.cache_result(query, response_content, simulated_cost)

            self._record_query(query, result)
            return result

        except Exception as e:
            error_result = {
                "error": str(e),
                "cached": False,
                "latency": time.time() - start_time,
                "cost": 0,
                "tokens": 0
            }
            self._record_query(query, error_result)
            return error_result

    def _record_query(self, query: str, result: Dict):
        """Record query for analysis"""
        self.metrics["query_history"].append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "result": result
        })

    def get_metrics_summary(self) -> Dict:
        """Get optimization metrics"""

        cache_rate = (
            self.metrics["cache_hits"] / self.metrics["total_queries"] * 100
            if self.metrics["total_queries"] > 0 else 0
        )

        avg_cost = (
            self.metrics["total_cost"] / self.metrics["total_queries"]
            if self.metrics["total_queries"] > 0 else 0
        )

        avg_latency = (
            sum(q["result"].get("latency", 0) for q in self.metrics["query_history"]) /
            len(self.metrics["query_history"])
            if self.metrics["query_history"] else 0
        )

        # Calculate optimization effectiveness
        total_possible_cost = self.metrics["total_cost"] + self.metrics["cost_saved"]
        optimization_effectiveness = (
            (self.metrics["cost_saved"] / total_possible_cost) * 100
            if total_possible_cost > 0 else 0
        )

        return {
            "cache_hit_rate": f"{cache_rate:.1f}%",
            "total_queries": self.metrics["total_queries"],
            "average_cost_per_query": f"${avg_cost:.4f}",
            "average_latency": f"{avg_latency:.3f}s",
            "total_cost": f"${self.metrics['total_cost']:.2f}",
            "total_cost_saved": f"${self.metrics['cost_saved']:.2f}",
            "total_tokens": self.metrics["total_tokens"],
            "optimization_effectiveness": f"{optimization_effectiveness:.1f}%",
            "cache_hits": self.metrics["cache_hits"],
        }

    def analyze_query_patterns(self) -> Dict:
        """Analyze patterns in query history"""
        if not self.metrics["query_history"]:
            return {"message": "No queries recorded yet"}

        # Analyze complexity distribution
        complexity_counts = {}
        cost_by_complexity = {}
        latency_by_complexity = {}

        for record in self.metrics["query_history"]:
            result = record["result"]
            complexity = result.get("complexity", "unknown")

            complexity_counts[complexity] = complexity_counts.get(complexity, 0) + 1

            if complexity not in cost_by_complexity:
                cost_by_complexity[complexity] = []
                latency_by_complexity[complexity] = []

            cost_by_complexity[complexity].append(result.get("cost", 0))
            latency_by_complexity[complexity].append(result.get("latency", 0))

        # Calculate averages
        analysis = {}
        for complexity in complexity_counts:
            count = complexity_counts[complexity]
            avg_cost = sum(cost_by_complexity[complexity]) / count
            avg_latency = sum(latency_by_complexity[complexity]) / count

            analysis[complexity] = {
                "count": count,
                "percentage": (count / len(self.metrics["query_history"])) * 100,
                "average_cost": avg_cost,
                "average_latency": avg_latency
            }

        return {
            "total_queries_analyzed": len(self.metrics["query_history"]),
            "complexity_analysis": analysis,
            "most_common_complexity": max(complexity_counts, key=complexity_counts.get),
        }


async def main():
    """Example usage of the cost-optimized agent"""
    print("Cost-Optimized Agent Demo")
    print("=" * 50)

    # Create agent with sample tools
    tools = create_sample_tools()
    agent = CostOptimizedAgent(tools)

    # Test queries of varying complexity
    test_queries = [
        "What's the weather in New York?",  # Simple
        "What's the weather in New York today?",  # Similar to first (should hit cache)
        "Calculate 15% tip on a $87.50 bill",  # Simple
        "Compare the performance of renewable energy vs fossil fuels",  # Complex
        "Send an email to my team about tomorrow's meeting",  # Medium
        "What are the latest AI research breakthroughs?",  # Medium
        "How's the weather in NYC?",  # Similar to first (should hit cache)
    ]

    print(f"Processing {len(test_queries)} queries...\n")

    # Process each query
    for i, query in enumerate(test_queries, 1):
        print(f"Query {i}: {query}")
        result = await agent.execute(query)

        print(f"  Result: {result['response'].get('answer', 'Error occurred')[:100]}...")
        print(f"  Cached: {'Yes' if result['cached'] else 'No'}")
        print(f"  Model: {result.get('model', 'N/A')}")
        print(f"  Cost: ${result['cost']:.4f}")
        print(f"  Latency: {result['latency']:.3f}s")
        if result.get('tools_used'):
            print(f"  Tools: {', '.join(result['tools_used'])}")
        print()

    # Display metrics
    print("Performance Metrics:")
    print("=" * 30)
    metrics = agent.get_metrics_summary()
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ').title()}: {value}")

    print(f"\nQuery Pattern Analysis:")
    print("=" * 30)
    patterns = agent.analyze_query_patterns()
    if "complexity_analysis" in patterns:
        for complexity, data in patterns["complexity_analysis"].items():
            print(f"{complexity.title()}: {data['count']} queries ({data['percentage']:.1f}%)")
            print(f"  Avg cost: ${data['average_cost']:.4f}")
            print(f"  Avg latency: {data['average_latency']:.3f}s")


if __name__ == "__main__":
    asyncio.run(main())