# AI Agent Observability System

This project implements a comprehensive observability system for production AI agents, extracted from Module 4, Task 1. It provides tracing, monitoring, alerting, and evaluation capabilities for LangChain-based agents.

## Overview

The system consists of four main components:

1. **ObservabilitySetup** (`observability_setup.py`) - LangSmith integration and project setup
2. **MonitoredAgent** (`monitored_agent.py`) - Agent wrapper with comprehensive monitoring
3. **EvaluationDatasetBuilder** (`evaluation_dataset.py`) - Creates evaluation datasets from production data
4. **PerformanceMonitor** (`performance_monitor.py`) - Performance alerts and monitoring

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     User Request                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│                  Agent Executor                          │
│  ┌─────────────────────────────────────────────────┐    │
│  │            Monitoring Wrapper                    │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │  • Start timer                            │  │    │
│  │  │  • Initialize tracing context             │  │    │
│  │  │  • Capture input metadata                 │  │    │
│  │  └───────────────┬───────────────────────────┘  │    │
│  │                  ▼                              │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │         Execute Agent Logic               │  │    │
│  │  │  ┌─────────────┐  ┌─────────────┐       │  │    │
│  │  │  │  LLM Calls  │─▶│  Tool Calls │       │  │    │
│  │  │  └─────────────┘  └─────────────┘       │  │    │
│  │  └───────────────┬───────────────────────────┘  │    │
│  │                  ▼                              │    │
│  │  ┌───────────────────────────────────────────┐  │    │
│  │  │  • Capture metrics (latency, tokens)      │  │    │
│  │  │  • Log results and errors                 │  │    │
│  │  │  • Send to monitoring services            │  │    │
│  │  └───────────────────────────────────────────┘  │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┬──────────────┐
        ▼            ▼            ▼              ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│LangSmith │  │  Logs    │  │ Metrics  │  │  Alerts  │
│ Tracing  │  │ (JSON)   │  │Dashboard │  │ (Errors) │
└──────────┘  └──────────┘  └──────────┘  └──────────┘
```

## Setup Instructions

### 1. Python Environment Setup

Create a virtual environment and install dependencies:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install langchain langsmith python-dotenv openai
```

### 2. Environment Configuration

Create a `.env` file in the project root with your API keys:

```env
# LangSmith Configuration
LANGCHAIN_API_KEY=your-langsmith-api-key-here
LANGCHAIN_PROJECT=production-agents
LANGCHAIN_TRACING_V2=true

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your-openai-api-key-here

# Optional: Other LLM providers
ANTHROPIC_API_KEY=your-anthropic-api-key-here
COHERE_API_KEY=your-cohere-api-key-here
```

### 3. LangSmith Account Setup

1. Sign up for a LangSmith account at [smith.langchain.com](https://smith.langchain.com)
2. Create a new API key in your account settings
3. Add the API key to your `.env` file

## Usage Examples

### Basic Usage

```python
from observability_setup import ObservabilitySetup
from monitored_agent import MonitoredAgent
from langchain.agents import AgentExecutor
# Your agent setup code here

# Initialize observability
obs_setup = ObservabilitySetup()

# Wrap your agent with monitoring
monitored = MonitoredAgent(your_agent_executor, "my-agent")

# Run with full monitoring
result = monitored.run_with_monitoring(
    "What is the weather like today?",
    metadata={"user_id": "123", "session": "abc"}
)

print(f"Result: {result['result']}")
print(f"Metrics: {result['metrics']}")
```

### Performance Monitoring

```python
from performance_monitor import PerformanceMonitor

# Initialize with custom thresholds
monitor = PerformanceMonitor({
    "latency_p95": 5.0,      # 5 second max latency
    "error_rate": 0.02,      # 2% error rate
    "cost_per_request": 0.25  # $0.25 per request
})

# Record metrics and check alerts
metrics = {
    "latency_seconds": 3.2,
    "total_cost_usd": 0.15,
    "error": False
}

alerts = monitor.record_metrics(metrics)
if alerts:
    print(f"Alerts: {alerts}")

# Get performance summary
summary = monitor.get_performance_summary()
print(summary)
```

### Creating Evaluation Datasets

```python
from evaluation_dataset import EvaluationDatasetBuilder

# Initialize builder
builder = EvaluationDatasetBuilder()

# Create sample dataset
dataset = builder.create_sample_dataset()
print(f"Created dataset: {dataset.id}")

# Or create from production data
production_runs = [
    {
        "query": "User question here",
        "result": "Agent response here",
        "metrics": {"latency_seconds": 2.1, "total_cost_usd": 0.05}
    }
    # ... more runs
]

builder.create_from_production(production_runs)
```

## Running the Components

### 1. Test Observability Setup

```bash
python observability_setup.py
```

Expected output:
```
✓ Connected to LangSmith project: production-agents
ObservabilitySetup initialized successfully!
```

### 2. Test Performance Monitor

```bash
python performance_monitor.py
```

This will run sample metrics through the monitor and demonstrate alerting.

### 3. Test Evaluation Dataset Builder

```bash
python evaluation_dataset.py
```

This creates a sample evaluation dataset in LangSmith.

### 4. Integration Example

Create an `example_usage.py` file:

```python
from dotenv import load_dotenv
from observability_setup import ObservabilitySetup
from monitored_agent import MonitoredAgent
from performance_monitor import PerformanceMonitor

# Load environment variables
load_dotenv()

def main():
    # Initialize components
    obs_setup = ObservabilitySetup()
    monitor = PerformanceMonitor()

    print("Observability system initialized!")
    print(f"Project: {obs_setup.project_name}")
    print(f"Tracer: {'✓' if obs_setup.tracer else '✗'}")

    # Example metrics
    sample_metrics = {
        "latency_seconds": 2.5,
        "total_cost_usd": 0.02,
        "total_tokens": 150
    }

    alerts = monitor.record_metrics(sample_metrics)
    print(f"Alerts: {alerts if alerts else 'None'}")

if __name__ == "__main__":
    main()
```

## Key Features

### 🔍 **Comprehensive Tracing**
- Automatic LangSmith integration
- Request/response logging
- Token usage tracking
- Cost monitoring

### 📊 **Performance Monitoring**
- Configurable alert thresholds
- Rolling metrics windows
- Cost limit enforcement
- Latency tracking

### 📈 **Evaluation Datasets**
- Auto-generation from production data
- Quality filtering
- Metadata preservation
- LangSmith integration

### 🚨 **Alerting System**
- Real-time performance alerts
- Cost threshold monitoring
- Error rate tracking
- Structured logging

## Best Practices

### 1. Selective Tracing in Production
```python
# Sample only 10% of requests in high-traffic production
if monitor.should_trace_request(sample_rate=0.1):
    # Enable tracing for this request
    pass
```

### 2. Structured Logging
```python
import json
logger.info(json.dumps({
    "event": "agent_start",
    "request_id": request_id,
    "tokens": token_count
}))
```

### 3. Cost Management
```python
# Set spending limits
if monitor.cost_limit_check(cost, limit=1.00):
    raise ValueError("Cost limit exceeded")
```

### 4. Error Handling
All components include comprehensive error handling with fallback options when external services are unavailable.

## Troubleshooting

### Common Issues

**1. LangSmith Connection Error**
- Verify your `LANGCHAIN_API_KEY` is correct
- Check internet connection
- Ensure LangSmith service is available

**2. Import Errors**
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check virtual environment is activated

**3. Environment Variables Not Loading**
- Verify `.env` file is in the correct location
- Check file permissions
- Ensure `python-dotenv` is installed

### Dependencies

Create a `requirements.txt` file:
```txt
langchain>=0.1.0
langsmith>=0.1.0
python-dotenv>=0.19.0
openai>=1.0.0
```

## Monitoring Checklist

- [ ] LangSmith API key configured in `.env`
- [ ] Project created in LangSmith
- [ ] Tracing enabled for agent executor
- [ ] Cost tracking implemented
- [ ] Structured logging in place
- [ ] Error handling with context
- [ ] Performance thresholds defined
- [ ] Evaluation dataset created
- [ ] Alerts configured for anomalies
- [ ] Sampling strategy for high traffic

## Contributing

1. Follow the existing code structure and patterns
2. Add comprehensive error handling
3. Include structured logging
4. Add appropriate documentation
5. Test with actual agent executors

## License

This code is provided as educational material for the Advanced Agentic AI Systems course.