#!/usr/bin/env python3
"""
Main script to demonstrate the specialized agent system.
"""

from orchestrator import SpecializedAgentSystem


def main():
    """Main function to run example tasks with the specialized agent system."""

    print("=== Specialized Agent System Demo ===\n")

    # Initialize the agent system
    system = SpecializedAgentSystem()

    # Example tasks for each agent type
    tasks = [
        {
            "description": "Research Task",
            "task": "Find the latest developments in quantum computing from 2024"
        },
        {
            "description": "Analysis Task",
            "task": "Calculate the compound annual growth rate from these numbers: [100, 120, 145, 178, 210]"
        },
        {
            "description": "Writing Task",
            "task": "Create an executive summary of these findings for the board of directors"
        }
    ]

    # Execute each task
    for i, task_info in enumerate(tasks, 1):
        print(f"\n{'='*50}")
        print(f"Task {i}: {task_info['description']}")
        print(f"{'='*50}")
        print(f"Request: {task_info['task']}")
        print("-" * 50)

        try:
            result = system.execute(task_info['task'])

            if result['success']:
                print(f"✅ Agent Used: {result['agent']}")
                print(f"📊 Iterations: {result['metadata']['iterations']}")
                print(f"🔧 Tools Used: {', '.join(result['metadata']['tools_used'])}")
                print(f"\n📝 Result:\n{result['result']}")
            else:
                print(f"❌ Error: {result['error']}")

        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    print(f"\n{'='*50}")
    print("Demo completed!")
    print("Check the ./outputs directory for any generated files.")


if __name__ == "__main__":
    main()