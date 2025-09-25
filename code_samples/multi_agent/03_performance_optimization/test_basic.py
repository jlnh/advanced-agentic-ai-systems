"""
Basic test to verify the code structure works without API calls.
"""

import os
from dotenv import load_dotenv

from agent_factory import create_optimized_system
from task_models import Task

# Load environment variables (will use mock agents if no API keys)
load_dotenv()

def test_basic_functionality():
    """Test basic functionality without external API calls"""

    print("🧪 Testing Basic Functionality")
    print("=" * 40)

    try:
        # Create the optimized system (should use mock agents)
        print("Creating optimized system...")
        orchestrator = create_optimized_system()
        print("✅ System created successfully")

        # Create simple test tasks
        print("\nCreating test tasks...")
        tasks = [
            Task(id="test1", description="Test task 1",
                 agent_type="research", dependencies=[], priority=1),
            Task(id="test2", description="Test task 2",
                 agent_type="analysis", dependencies=["test1"], priority=2)
        ]
        print(f"✅ Created {len(tasks)} test tasks")

        # Execute tasks
        print("\nExecuting tasks...")
        results = orchestrator.execute_parallel(tasks)
        print("✅ Tasks executed successfully")

        # Display results
        print("\n📊 Results:")
        for task_id, result in results.items():
            status = "✅" if result.get("success", False) else "❌"
            output = result.get("output", result.get("error", "No output"))[:50]
            print(f"  {status} {task_id}: {output}...")

        # Display metrics
        print("\n📈 Metrics:")
        metrics = orchestrator.metrics.get_summary()
        print(f"  Duration: {metrics['total_duration']:.2f}s")
        print(f"  Speedup: {metrics['parallel_speedup']:.1f}x")
        print(f"  Cost: ${metrics['total_cost']:.3f}")

        print("\n✅ Basic test completed successfully!")
        return True

    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_basic_functionality()
    exit(0 if success else 1)