"""
Test functions for memory system capabilities and optimization.
"""

import time
from datetime import datetime


def test_memory_learning(memory_agent, long_memory):
    """Test that agent learns and remembers across interactions"""

    print("\n=== Memory Learning Test ===")

    # First interaction - establish preferences
    print("\n1. First interaction:")
    result1 = memory_agent.invoke("I'm interested in quantum computing research. I prefer technical papers over popular articles.")
    print(f"Response: {result1['output'][:200]}...")

    # Second interaction - test short-term memory
    print("\n2. Second interaction (same session):")
    result2 = memory_agent.invoke("Can you find 3 recent papers on quantum algorithms?")
    print(f"Response: {result2['output'][:200]}...")

    # End session to trigger insight extraction
    print("\n3. Ending session...")
    summary = memory_agent.end_session()
    print(f"Session summary: {summary[:150]}...")

    # New session - test long-term memory
    print("\n4. New session - testing long-term memory:")
    result3 = memory_agent.invoke("Find more quantum research like before")
    print(f"Response: {result3['output'][:200]}...")

    # Check user profile
    print("\n5. User profile learned:")
    profile = long_memory.get_user_profile()
    print(f"Preferences: {len(profile['preferences'])} stored")
    print(f"Expertise areas: {profile['expertise_areas']}")


def test_memory_optimization(memory_agent, short_memory, long_memory):
    """Test memory system performance and token usage"""

    print("\n=== Memory Optimization Test ===")

    # Track token usage with memory
    start_time = time.time()

    # Simulate multiple interactions
    for i in range(5):
        query = f"Test query {i+1}: find information about AI topic {i+1}"
        result = memory_agent.invoke(query)
        print(f"Query {i+1} processed")

    end_time = time.time()

    # Check memory efficiency
    context = short_memory.get_context()
    relevant_memories = long_memory.find_relevant_context("AI topic", k=5)

    print(f"Processing time: {end_time - start_time:.2f} seconds")
    print(f"Short-term memory size: {len(str(context))} characters")
    print(f"Long-term memories found: {len(relevant_memories)}")

    # Memory cleanup simulation
    summary = memory_agent.end_session()
    print(f"Session compressed to: {len(summary)} characters")


def run_all_tests(memory_agent, short_memory, long_memory):
    """Run comprehensive memory system tests"""
    print("🧠 Starting Memory System Tests")

    try:
        test_memory_learning(memory_agent, long_memory)
        test_memory_optimization(memory_agent, short_memory, long_memory)
        print("\n✅ All memory tests completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")


if __name__ == "__main__":
    print("Memory system test functions loaded.")
    print("To run tests, initialize your memory components and call:")
    print("run_all_tests(memory_agent, short_memory, long_memory)")