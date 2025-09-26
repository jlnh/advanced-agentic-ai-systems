"""
Example Usage
Demonstrates how to use the observability system components together.
"""

from dotenv import load_dotenv
from observability_setup import ObservabilitySetup
from monitored_agent import MonitoredAgent
from performance_monitor import PerformanceMonitor
from evaluation_dataset import EvaluationDatasetBuilder

# Load environment variables
load_dotenv()


def main():
    """Main example demonstrating observability system usage"""
    print("🚀 Initializing AI Agent Observability System...")

    # Initialize components
    try:
        obs_setup = ObservabilitySetup()
        monitor = PerformanceMonitor()
        dataset_builder = EvaluationDatasetBuilder()

        print("✅ All components initialized successfully!")
        print(f"📊 Project: {obs_setup.project_name}")
        print(f"🔍 Tracer: {'✓ Connected' if obs_setup.tracer else '✗ Not connected'}")

    except Exception as e:
        print(f"❌ Initialization error: {e}")
        return

    # Demonstrate performance monitoring
    print("\n📈 Testing Performance Monitoring...")

    sample_metrics = [
        {
            "latency_seconds": 2.5,
            "total_cost_usd": 0.02,
            "total_tokens": 150,
            "error": False
        },
        {
            "latency_seconds": 12.0,  # This should trigger latency alert
            "total_cost_usd": 0.60,   # This should trigger cost alert
            "total_tokens": 800,
            "error": False
        },
        {
            "latency_seconds": 3.2,
            "total_cost_usd": 0.03,
            "total_tokens": 180,
            "error": True  # This contributes to error rate
        }
    ]

    for i, metrics in enumerate(sample_metrics, 1):
        print(f"  Request {i}: ", end="")
        alerts = monitor.record_metrics(metrics)
        if alerts:
            print(f"🚨 ALERTS: {', '.join(alerts)}")
        else:
            print("✅ No alerts")

    # Show performance summary
    print("\n📊 Performance Summary:")
    summary = monitor.get_performance_summary()
    for key, value in summary.items():
        if key != "timestamp":
            print(f"  {key.replace('_', ' ').title()}: {value}")

    # Test sampling for production
    print(f"\n🎲 Sampling Test (10% rate):")
    traced_requests = sum(1 for _ in range(100) if monitor.should_trace_request(0.1))
    print(f"  Out of 100 requests, {traced_requests} would be traced")

    # Demonstrate evaluation dataset creation
    print(f"\n📚 Testing Evaluation Dataset Creation...")
    try:
        dataset = dataset_builder.create_sample_dataset()
        print(f"  ✅ Sample dataset created with ID: {dataset.id}")
    except Exception as e:
        print(f"  ⚠️  Dataset creation failed: {e}")
        print("     Make sure LANGCHAIN_API_KEY is set correctly")

    # Show MonitoredAgent usage example
    print(f"\n🤖 MonitoredAgent Usage Example:")
    print("  # Your typical usage would be:")
    print("  from langchain.agents import AgentExecutor")
    print("  # ... create your agent executor ...")
    print("  monitored = MonitoredAgent(agent_executor, 'my-agent')")
    print("  result = monitored.run_with_monitoring('What is the weather?')")
    print("  print(result['metrics'])  # View performance data")

    print(f"\n✨ Observability system demo completed!")
    print(f"💡 Next steps:")
    print(f"   1. Set up your actual agent executor")
    print(f"   2. Wrap it with MonitoredAgent")
    print(f"   3. Monitor the logs and LangSmith dashboard")
    print(f"   4. Adjust thresholds based on your needs")


if __name__ == "__main__":
    main()