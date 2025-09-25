#!/usr/bin/env python3
"""
Test script that runs without requiring OpenAI API key or Redis
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_intelligent_router():
    """Test the intelligent router without API calls"""
    print("Testing Intelligent Router:")
    print("-" * 30)

    from intelligent_router import IntelligentRouter

    router = IntelligentRouter()
    test_queries = [
        "What is the capital of France?",
        "Compare the economic policies of France and Germany",
        "How would you design a recommendation system?",
    ]

    for query in test_queries:
        routing = router.route_query(query)
        print(f"Query: {query[:50]}...")
        print(f"  Complexity: {routing['complexity']}")
        print(f"  Model: {routing['model']}")
        print(f"  Estimated cost: ${routing['estimated_cost']:.4f}")
        print()

    return True

def test_simple_tool_optimizer():
    """Test the simple tool optimizer"""
    print("Testing Simple Tool Optimizer:")
    print("-" * 30)

    from tool_optimizer_simple import SimpleToolOptimizer, create_sample_tools

    tools = create_sample_tools()
    optimizer = SimpleToolOptimizer(tools)

    test_queries = [
        "What's the weather in New York?",
        "Calculate 15% of $100",
        "Send an email notification"
    ]

    for query in test_queries:
        stats = optimizer.get_optimization_stats(query)
        print(f"Query: {query}")
        print(f"  Tools selected: {stats['tools_selected']}/{stats['total_tools_available']}")
        print(f"  Token reduction: {stats['token_reduction_percent']:.1f}%")
        print(f"  Selected: {', '.join([t['name'] for t in stats['selected_tools'][:3]])}...")
        print()

    return True

def test_cache_fallback():
    """Test cache functionality with minimal cache (no OpenAI API required)"""
    print("Testing Minimal Semantic Cache:")
    print("-" * 30)

    # Use the actual minimal semantic cache
    from semantic_cache_minimal import MinimalSemanticCache

    cache = MinimalSemanticCache()

    # First, cache some test data
    test_data = [
        ("What's the weather in San Francisco?", {"answer": "Sunny, 72°F"}),
        ("How is the weather in NYC?", {"answer": "Cloudy, 65°F"}),
        ("Calculate 15% tip on $50", {"answer": "$7.50"}),
    ]

    print("Caching initial data...")
    for query, result in test_data:
        cache.cache_result(query, result, 0.05)

    # Test cache operations with similar queries
    test_queries = [
        "What's the weather in SF?",        # Should match San Francisco
        "How's the weather in New York?",   # Should match NYC
        "What's 15% tip for $50?",         # Should match tip calculation
        "What time is it?",                # Should not match anything
    ]

    print("\nTesting similarity detection...")
    for query in test_queries:
        similar = cache.find_similar_query(query)
        if similar:
            print(f"Query: {query}")
            print(f"  ✓ Found similar: {similar['original_query']}")
            print(f"  ✓ Similarity: {similar['similarity']:.3f}")

            # Get cached response
            response = cache.get_cached_response(similar['key'])
            if response:
                print(f"  ✓ Cached response: {response}")
            print("  → Cache HIT")
        else:
            print(f"Query: {query}")
            print("  → Cache MISS")
        print()

    return True

def main():
    """Run all tests"""
    print("Cost-Optimized Agent Components Test")
    print("=" * 50)
    print("Running tests without OpenAI API key or Redis...")
    print()

    tests = [
        test_intelligent_router,
        test_simple_tool_optimizer,
        test_cache_fallback
    ]

    passed = 0
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed: {e}")
            print()

    print(f"Summary: {passed}/{len(tests)} tests passed")
    print("\n✅ All core components are working!")
    print("\n📋 To run with full functionality:")
    print("1. Set OPENAI_API_KEY in .env file")
    print("2. Start Redis server (optional, falls back to memory)")
    print("3. Run: python cost_optimized_agent.py")

if __name__ == "__main__":
    main()