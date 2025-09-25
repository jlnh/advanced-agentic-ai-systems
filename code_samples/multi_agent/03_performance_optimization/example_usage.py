"""
Example usage of the optimized multi-agent system.
Demonstrates parallel execution, cost optimization, and monitoring.
"""

import os
import time
from dotenv import load_dotenv

from agent_factory import create_optimized_system
from task_models import Task
from optimization_utils import AdaptiveOptimizer

# Load environment variables
load_dotenv()


def run_example():
    """Example: Complex parallel execution with monitoring"""

    print("🚀 Multi-Agent Performance Optimization Example")
    print("=" * 50)

    try:
        # Create the optimized system
        print("Initializing optimized orchestrator...")
        orchestrator = create_optimized_system()
        print("✅ System initialized")

        # Create adaptive optimizer
        print("Setting up adaptive optimizer...")
        optimizer = AdaptiveOptimizer(orchestrator)
        print("✅ Optimizer ready")

        # Define tasks with dependencies
        print("\nDefining task pipeline...")
        tasks = [
            # Parallel research tasks
            Task(id="r1", description="Research AI market size",
                 agent_type="research", dependencies=[], priority=1),
            Task(id="r2", description="Research competitor landscape",
                 agent_type="research", dependencies=[], priority=1),
            Task(id="r3", description="Research technology trends",
                 agent_type="research", dependencies=[], priority=2),

            # Analysis depends on all research
            Task(id="a1", description="Analyze market opportunities",
                 agent_type="analysis", dependencies=["r1", "r2", "r3"], priority=1),

            # Writing depends on analysis
            Task(id="w1", description="Write executive summary",
                 agent_type="writing", dependencies=["a1"], priority=1),

            # Review depends on writing
            Task(id="rev1", description="Review and polish summary",
                 agent_type="review", dependencies=["w1"], priority=3)
        ]
        print(f"✅ Created {len(tasks)} tasks with dependencies")

    except Exception as e:
        print(f"❌ Error during initialization: {str(e)}")
        return {}

    # Execute with monitoring
    print("\n🚀 Starting optimized execution...")
    start_time = time.time()

    try:
        results = orchestrator.execute_parallel(tasks)
        print("✅ Execution completed")
    except Exception as e:
        print(f"❌ Execution failed: {str(e)}")
        return {}

    # Display performance metrics
    metrics = orchestrator.metrics.get_summary()
    print(f"\n📊 Performance Metrics:")
    print(f"  Total Duration: {metrics['total_duration']:.2f}s")
    print(f"  Parallel Speedup: {metrics['parallel_speedup']:.1f}x")
    print(f"  Total Tokens: {metrics['total_tokens']:,}")
    print(f"  Total Cost: ${metrics['total_cost']:.3f}")
    print(f"  Cache Hit Rate: {metrics['cache_hit_rate']*100:.1f}%")
    print(f"  Error Rate: {metrics['error_rate']*100:.1f}%")

    # Display cost breakdown
    cost_breakdown = orchestrator.cost_controller.get_cost_breakdown()
    print(f"\n💰 Cost Analysis:")
    print(f"  Budget Used: ${cost_breakdown['total']:.3f} / ${orchestrator.cost_limit:.2f}")
    print(f"  Average per Task: ${cost_breakdown['average_per_task']:.3f}")
    for agent, cost in cost_breakdown['by_agent'].items():
        print(f"  {agent}: ${cost:.3f}")

    # Get optimization suggestions
    suggestions = orchestrator.cost_controller.suggest_optimizations()
    if suggestions:
        print(f"\n💡 Optimization Suggestions:")
        for suggestion in suggestions:
            print(f"  • {suggestion}")

    # Apply adaptive optimizations
    print(f"\n🔧 Applying adaptive optimizations...")
    optimizer.analyze_and_optimize(metrics)

    # Display results
    print(f"\n✅ Execution Results:")
    for task_id, result in results.items():
        status = "✅" if result.get("success") else "❌"
        output = result.get("output", result.get("error", "No output"))[:100]
        print(f"  {status} {task_id}: {output}...")

    return results


def run_batch_processing_example():
    """Example: Batch processing for cost optimization"""

    try:
        from optimization_utils import IntelligentBatcher

        print("\n🎯 Batch Processing Example")
        print("-" * 30)

        batcher = IntelligentBatcher(batch_size=3, wait_time=2.0)

        # Submit similar tasks for batching
        batch_tasks = [
            Task(f"batch_{i}", f"Analyze data point {i}", "analysis", [])
            for i in range(5)  # Reduced from 8 to 5 for faster demo
        ]

        print(f"Submitting {len(batch_tasks)} tasks for batch processing...")

        # Submit tasks and collect futures
        futures = []
        for task in batch_tasks:
            future = batcher.add_task(task)
            futures.append(future)

        # Wait for results with timeout
        results = []
        for i, future in enumerate(futures):
            try:
                result = future.result(timeout=10)  # Reduced timeout
                results.append(result)
            except Exception as e:
                print(f"❌ Batch task {i} failed: {e}")

        print(f"✅ Completed {len(results)} batched tasks")

    except Exception as e:
        print(f"❌ Batch processing example failed: {str(e)}")
        print("This is normal if running without full dependencies")


def run_dynamic_model_selection_example():
    """Example: Dynamic model selection based on task complexity"""

    try:
        from optimization_utils import DynamicModelSelector

        print("\n🤖 Dynamic Model Selection Example")
        print("-" * 40)

        selector = DynamicModelSelector()

        # Test tasks of different complexities
        test_tasks = [
            Task("simple", "Find the capital of France", "research"),
            Task("moderate", "Analyze market trends for Q3", "analysis"),
            Task("complex", "Design a comprehensive marketing strategy", "writing")
        ]

        budget_remaining = 0.20

        print(f"Budget remaining: ${budget_remaining:.2f}")
        print()

        for task in test_tasks:
            selected_model = selector.select_model(task, budget_remaining)
            complexity = selector._assess_complexity(task.description)

            print(f"Task: {task.description[:40]}...")
            print(f"  Complexity: {complexity}")
            print(f"  Selected Model: {selected_model}")
            print()

    except Exception as e:
        print(f"❌ Model selection example failed: {str(e)}")
        print("This is normal if running without full dependencies")


if __name__ == "__main__":
    print("🚀 Multi-Agent Performance Optimization Examples")
    print("=" * 50)

    # Run main example
    run_example()

    # Run additional examples
    run_batch_processing_example()
    run_dynamic_model_selection_example()

    print("\n✅ All examples completed!")