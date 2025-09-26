"""
Monitored Agent
Wraps agent executor with comprehensive monitoring and observability.
"""

import time
import logging
import traceback
import json
from typing import Dict, Any
from datetime import datetime
from dotenv import load_dotenv
from langchain.callbacks import get_openai_callback
from observability_setup import ObservabilitySetup

# Load environment variables
load_dotenv()


class MonitoredAgent:
    def __init__(self, agent_executor, name="default-agent"):
        self.agent = agent_executor
        self.name = name
        self.setup_logging()
        self.metrics = {"total_requests": 0, "total_errors": 0}

    def setup_logging(self):
        """Configure structured logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(f"agent.{self.name}")

    def run_with_monitoring(self, query: str, metadata: Dict[str, Any] = None):
        """Execute agent with full observability"""
        request_id = f"{self.name}-{int(time.time() * 1000)}"
        start_time = time.time()

        # Create monitoring context
        context = {
            "request_id": request_id,
            "agent_name": self.name,
            "query": query,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        }

        try:
            # Track token usage and costs
            with get_openai_callback() as cb:
                # Add LangSmith tracing
                obs_setup = ObservabilitySetup()
                if hasattr(self.agent, 'callbacks') and obs_setup.tracer:
                    self.agent.callbacks = [obs_setup.tracer]

                # Execute the agent
                self.logger.info(f"Starting request {request_id}")
                result = self.agent.invoke({"input": query})

                # Capture metrics
                execution_time = time.time() - start_time
                metrics = {
                    "latency_seconds": execution_time,
                    "total_tokens": cb.total_tokens,
                    "prompt_tokens": cb.prompt_tokens,
                    "completion_tokens": cb.completion_tokens,
                    "total_cost_usd": cb.total_cost,
                    "successful_completion": cb.successful_requests
                }

                # Log success
                self._log_success(context, result, metrics)

                # Update aggregated metrics
                self.metrics["total_requests"] += 1

                return {
                    "result": result,
                    "metrics": metrics,
                    "request_id": request_id
                }

        except Exception as e:
            # Log error with full context
            self._log_error(context, e)
            self.metrics["total_errors"] += 1
            raise

    def _log_success(self, context: Dict, result: Any, metrics: Dict):
        """Log successful execution with metrics"""
        log_entry = {
            **context,
            "status": "success",
            "metrics": metrics,
            "result_preview": str(result)[:200]  # First 200 chars
        }

        self.logger.info(json.dumps(log_entry))

        # Alert on high costs
        if metrics["total_cost_usd"] > 0.50:
            self.logger.warning(
                f"High cost query: ${metrics['total_cost_usd']:.2f} "
                f"for request {context['request_id']}"
            )

    def _log_error(self, context: Dict, error: Exception):
        """Log errors with full context for debugging"""
        log_entry = {
            **context,
            "status": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc()
        }

        self.logger.error(json.dumps(log_entry))

    def get_metrics(self):
        """Return current agent metrics"""
        return self.metrics.copy()


if __name__ == "__main__":
    # Example usage (requires an actual agent executor)
    print("MonitoredAgent class is ready for use with your agent executor!")
    print("Example usage:")
    print("  from langchain.agents import AgentExecutor")
    print("  # Create your agent executor")
    print("  monitored = MonitoredAgent(agent_executor, 'my-agent')")
    print("  result = monitored.run_with_monitoring('What is the weather?')")