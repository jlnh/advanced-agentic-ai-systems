"""
Test Examples for ReAct Agent

This module contains test cases demonstrating progressively complex tasks
for the ReAct agent from Module 1 Task 1.
"""

from react_agent import create_basic_agent, robust_agent_call, setup_environment


def run_basic_tests():
    """Run basic test queries to verify agent functionality."""
    # Setup environment
    setup_environment()

    # Create the agent
    print("Creating ReAct agent for testing...")
    agent_executor = create_basic_agent()

    # Define test queries with increasing complexity
    test_queries = [
        "What is 2+2?",                    # Basic arithmetic
        "What day is today?",              # Tool limitation test
        "Calculate the square root of 16"  # Mathematical operation
    ]

    print("\n" + "="*50)
    print("RUNNING BASIC TESTS")
    print("="*50)

    for i, query in enumerate(test_queries, 1):
        print(f"\nTest {i}: {query}")
        print("-" * 40)
        try:
            result = agent_executor.invoke({"input": query})
            print(f"✅ Success: {result['output']}")
        except Exception as e:
            print(f"❌ Failed: {e}")
            print("Check your API key, tool setup, and query complexity")


def run_progressive_tests():
    """Run progressively complex test cases."""
    # Setup environment
    setup_environment()

    # Create the agent
    print("Creating ReAct agent for progressive testing...")
    agent_executor = create_basic_agent()

    test_cases = [
        {
            "name": "Simple arithmetic",
            "query": "What is 25% of 1,380?",
            "description": "Basic percentage calculation"
        },
        {
            "name": "Multi-step calculation",
            "query": "Calculate the compound interest on $1000 at 5% annually for 3 years",
            "description": "Financial calculation requiring formula application"
        },
        {
            "name": "Data analysis",
            "query": "Create a list of numbers from 1 to 100, then find the sum of all prime numbers in that list",
            "description": "Complex task requiring list generation, prime detection, and summation"
        }
    ]

    print("\n" + "="*60)
    print("RUNNING PROGRESSIVE COMPLEXITY TESTS")
    print("="*60)

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']}")
        print(f"Description: {test_case['description']}")
        print(f"Query: {test_case['query']}")
        print("-" * 60)

        result = robust_agent_call(agent_executor, test_case['query'])
        print(f"Result: {result['output']}")
        print()


if __name__ == "__main__":
    print("ReAct Agent Test Suite")
    print("Choose test type:")
    print("1. Basic tests (quick verification)")
    print("2. Progressive tests (increasing complexity)")
    print("3. Both")

    choice = input("Enter your choice (1-3): ").strip()

    if choice == "1":
        run_basic_tests()
    elif choice == "2":
        run_progressive_tests()
    elif choice == "3":
        run_basic_tests()
        run_progressive_tests()
    else:
        print("Invalid choice. Running basic tests by default.")
        run_basic_tests()