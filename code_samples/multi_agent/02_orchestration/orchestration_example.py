"""
Practical Usage Example of the Multi-Agent Orchestration System
Demonstrates how to create and use the orchestrated system with complex requests.
"""

from supervisor_agent import SupervisorAgent
from specialized_agents import (
    create_researcher_agent,
    create_analyst_agent,
    create_writer_agent
)
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_orchestrated_system():
    """Create a fully orchestrated multi-agent system"""

    # Initialize specialized agents
    agents = {
        "researcher": create_researcher_agent(),
        "analyst": create_analyst_agent(),
        "writer": create_writer_agent()
    }

    # Create supervisor
    supervisor = SupervisorAgent(agents)

    return supervisor

def main():
    """Main function to demonstrate the orchestration system"""

    print("🚀 Initializing Multi-Agent Orchestration System...")
    system = create_orchestrated_system()

    # Test with increasingly complex requests
    test_requests = [
        # Simple sequential task
        "Find information about renewable energy trends in 2024",

        # Multi-step with dependencies
        "Research the top 3 AI companies, analyze their market positions, and create an investment summary",

        # Complex parallel and sequential mix
        """Research these three topics in parallel:
        1. Current state of quantum computing
        2. Latest developments in fusion energy
        3. Progress in brain-computer interfaces

        Then analyze which has the most commercial potential in the next 5 years,
        and write an executive briefing for investors."""
    ]

    for i, request in enumerate(test_requests, 1):
        print(f"\n{'='*60}")
        print(f"TEST {i}: Running orchestration example")
        print(f"{'='*60}")

        try:
            result = system.run(request)

            print(f"\n📈 Results:")
            print(f"Status: {result['status']}")
            print(f"Success Rate: {result['success_rate']*100:.1f}%")
            print(f"\nOutput Preview:")
            preview = result['output'][:500] + "..." if len(result['output']) > 500 else result['output']
            print(preview)

            # Display task breakdown
            print(f"\n📋 Task Breakdown:")
            for task_id, task_result in result['task_results'].items():
                status_emoji = "✅" if task_result['success'] else "❌"
                print(f"  {status_emoji} {task_id}: {task_result['task'].description[:60]}...")

        except Exception as e:
            print(f"❌ Error running example: {e}")

        print(f"\n{'='*60}\n")

if __name__ == "__main__":
    # Check if API key is available
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY environment variable not found!")
        print("Please set your OpenAI API key in the .env file.")
        exit(1)

    main()