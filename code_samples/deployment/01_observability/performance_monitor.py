"""
Performance Monitor
Implements performance alerts and monitoring for agent systems.
"""

import random
import json
import logging
from typing import Dict, List, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class PerformanceMonitor:
    def __init__(self, alert_thresholds: Dict[str, float] = None):
        self.thresholds = alert_thresholds or {
            "latency_p95": 10.0,  # 95th percentile latency in seconds
            "error_rate": 0.05,    # 5% error rate
            "cost_per_request": 0.50  # $0.50 per request
        }
        self.metrics_window = []  # Rolling window of metrics
        self.setup_logging()

    def setup_logging(self):
        """Configure logging for performance monitoring"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger("performance_monitor")

    def check_alerts(self, metrics: Dict[str, Any]) -> List[str]:
        """Check if metrics exceed thresholds"""
        alerts = []

        if metrics.get("latency_seconds", 0) > self.thresholds["latency_p95"]:
            alerts.append(f"High latency: {metrics['latency_seconds']:.2f}s")

        if metrics.get("total_cost_usd", 0) > self.thresholds["cost_per_request"]:
            alerts.append(f"High cost: ${metrics['total_cost_usd']:.2f}")

        # Check error rate if we have recent metrics
        if len(self.metrics_window) > 10:
            recent_errors = sum(1 for m in self.metrics_window[-10:] if m.get("error", False))
            error_rate = recent_errors / 10
            if error_rate > self.thresholds["error_rate"]:
                alerts.append(f"High error rate: {error_rate:.1%}")

        return alerts

    def record_metrics(self, metrics: Dict[str, Any]):
        """Record metrics and check for alerts"""
        # Add timestamp to metrics
        metrics["timestamp"] = datetime.utcnow().isoformat()

        # Add to rolling window (keep last 100 entries)
        self.metrics_window.append(metrics)
        if len(self.metrics_window) > 100:
            self.metrics_window.pop(0)

        # Check for alerts
        alerts = self.check_alerts(metrics)
        if alerts:
            alert_message = {
                "event": "performance_alert",
                "alerts": alerts,
                "metrics": metrics
            }
            self.logger.warning(json.dumps(alert_message))

        return alerts

    def should_trace_request(self, sample_rate: float = 0.1) -> bool:
        """Determine if request should be traced (sampling for high traffic)"""
        return random.random() < sample_rate

    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of recent performance metrics"""
        if not self.metrics_window:
            return {"message": "No metrics recorded yet"}

        recent_metrics = self.metrics_window[-10:] if len(self.metrics_window) >= 10 else self.metrics_window

        # Calculate averages
        avg_latency = sum(m.get("latency_seconds", 0) for m in recent_metrics) / len(recent_metrics)
        avg_cost = sum(m.get("total_cost_usd", 0) for m in recent_metrics) / len(recent_metrics)
        total_requests = len(recent_metrics)
        error_count = sum(1 for m in recent_metrics if m.get("error", False))

        return {
            "summary_period": "last_10_requests",
            "total_requests": total_requests,
            "average_latency_seconds": round(avg_latency, 2),
            "average_cost_usd": round(avg_cost, 4),
            "error_count": error_count,
            "error_rate": round(error_count / total_requests, 2) if total_requests > 0 else 0,
            "timestamp": datetime.utcnow().isoformat()
        }

    def cost_limit_check(self, cost: float, limit: float = 1.00) -> bool:
        """Check if cost exceeds limit and should block request"""
        if cost > limit:
            alert_msg = f"Cost limit exceeded: ${cost:.2f} > ${limit:.2f} - blocking request"
            self.logger.error(alert_msg)
            return True
        return False


# Best Practices Examples
class BestPracticesExamples:
    """Examples of monitoring best practices mentioned in the documentation"""

    @staticmethod
    def selective_tracing_example():
        """Example of selective tracing for production"""
        should_trace = random.random() < 0.1  # Trace 10% of requests
        return should_trace

    @staticmethod
    def structured_logging_example():
        """Example of structured vs unstructured logging"""
        logger = logging.getLogger("example")

        # Good: Structured, searchable
        good_log = {"event": "agent_start", "request_id": "123", "tokens": 500}
        logger.info(json.dumps(good_log))

        # Bad: Unstructured string (commented out)
        # logger.info(f"Starting agent with {tokens} tokens")

    @staticmethod
    def cost_alert_example(cb):
        """Example of cost alert implementation"""
        if cb.total_cost > 1.00:
            raise ValueError("Cost limit exceeded - blocking request")

    @staticmethod
    def tool_usage_tracking_example(agent_trace):
        """Example of tracking tool usage patterns"""
        tool_usage = {}
        # This would need actual agent trace data
        # for action in agent_trace.actions:
        #     tool_usage[action.tool] = tool_usage.get(action.tool, 0) + 1
        # Optimize or cache frequently used tools
        return tool_usage


if __name__ == "__main__":
    # Demonstration of performance monitoring
    monitor = PerformanceMonitor()

    # Simulate some metrics
    sample_metrics = [
        {"latency_seconds": 2.5, "total_cost_usd": 0.02, "error": False},
        {"latency_seconds": 15.0, "total_cost_usd": 0.75, "error": False},  # High latency, high cost
        {"latency_seconds": 3.2, "total_cost_usd": 0.03, "error": True},    # Error case
    ]

    print("Recording sample metrics and checking for alerts...")
    for i, metrics in enumerate(sample_metrics):
        print(f"\nRequest {i+1}:")
        alerts = monitor.record_metrics(metrics)
        if alerts:
            print(f"  ALERTS: {', '.join(alerts)}")
        else:
            print("  No alerts")

    print("\nPerformance Summary:")
    summary = monitor.get_performance_summary()
    print(json.dumps(summary, indent=2))