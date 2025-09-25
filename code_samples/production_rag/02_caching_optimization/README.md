# Intelligent Caching & Cost Optimization

This project demonstrates production-grade AI system optimization through intelligent caching, query routing, and resource management. It shows how to reduce AI API costs by 70-90% while improving response times.

## Overview

The system implements four key optimization strategies:

1. **Semantic Caching**: Cache responses based on query meaning, not exact text match
2. **Intelligent Query Routing**: Route queries to appropriate models (GPT-3.5 vs GPT-4) based on complexity
3. **Dynamic Tool Selection**: Select only relevant tools for each query to reduce token usage
4. **Cost-Optimized Agent**: Integrated system combining all optimization strategies

## Architecture

```
User Query → Query Analyzer → Semantic Cache Check → Model Router → Tool Optimizer → Execution → Response
                                   ↓ (cache miss)         ↓              ↓
                              Cache Storage ←──── Cost Tracking ←──── Selected Tools
```

## Files Structure

- `semantic_cache.py` - Semantic caching system with Redis backend
- `semantic_cache_minimal.py` - Lightweight caching with simple similarity matching
- `intelligent_router.py` - Query complexity analysis and model routing
- `tool_optimizer.py` - Dynamic tool selection based on query relevance (requires OpenAI API)
- `tool_optimizer_simple.py` - Simple tool selection using keyword matching
- `cost_optimized_agent.py` - Main agent integrating all optimization components
- `test_without_api.py` - Comprehensive test suite that works without APIs
- `langchain_compat.py` - Compatibility layer for different LangChain versions
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template

## Quick Start

**Test immediately (no setup required):**
```bash
python test_without_api.py
```

This demonstrates all optimization concepts with mock implementations.

## Setup Instructions

### 1. Prerequisites

- Python 3.8 or higher
- Redis server (optional - system falls back to memory cache)
- OpenAI API key (optional - for full functionality)

### 2. Environment Setup

```bash
# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration

```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your credentials
# Required for full functionality:
OPENAI_API_KEY=your_actual_openai_api_key

# Optional (uses defaults if not specified):
REDIS_HOST=localhost
REDIS_PORT=6379
```

## How to Run

### Individual Component Testing

**Test Intelligent Router:**
```bash
python intelligent_router.py
```

**Test Simple Tool Optimizer:**
```bash
python tool_optimizer_simple.py
```

**Test Minimal Semantic Cache:**
```bash
python semantic_cache_minimal.py
```

**Test Full System (requires OpenAI API key):**
```bash
python cost_optimized_agent.py
```

### Complete System Demo

```bash
python test_without_api.py
```

This runs all components with mock implementations and shows:
- Query routing based on complexity
- Tool optimization with 70%+ token reduction
- Semantic cache simulation with hit/miss detection
- Complete cost optimization workflow

## Expected Output

When running the complete demo:

```
Cost-Optimized Agent Components Test
==================================================

Testing Intelligent Router:
Query: What is the capital of France?
  Complexity: simple
  Model: gpt-3.5-turbo
  Estimated cost: $0.0008

Testing Tool Optimizer:
Query: What's the weather in New York?
  Tools selected: 5/20
  Token reduction: 70.3%
  Selected tools: web_search, weather_api, calculator...

Testing Semantic Cache:
Query: What's the weather in SF?
  ✓ Found similar: 'What's the weather in San Francisco?'
  ✓ Similarity: 0.939
  → Cache HIT

Summary: 3/3 tests passed
✅ All core components are working!
```

## Key Features Demonstrated

### 1. Semantic Caching
- Recognizes that "weather in New York" and "weather in NYC" are similar
- Achieves 30-50% cache hit rates with varied phrasing
- Saves ~$0.05 per cached query

### 2. Smart Model Routing
- Routes simple queries to GPT-3.5-turbo (10x cheaper)
- Uses GPT-4 only for complex analysis tasks
- Can reduce model costs by 70-80%

### 3. Dynamic Tool Selection
- Selects 3-5 most relevant tools from 20+ available
- Reduces prompt tokens by 60-70%
- Faster execution and lower costs

### 4. Cost Tracking
- Real-time cost monitoring
- Detailed metrics on savings and optimization effectiveness
- Query pattern analysis

## Production Considerations

### Performance Tuning
- Adjust similarity thresholds based on your use case
- Set appropriate cache TTL values for data freshness
- Monitor cache hit rates and optimize accordingly

### Scaling
- Use Redis Cluster for high-traffic applications
- Implement cache warming for common queries
- Add monitoring and alerting for cost anomalies

### Security
- Never cache sensitive information
- Implement proper API key rotation
- Use Redis AUTH in production

## Cost Savings Examples

| Scenario | Without Optimization | With Optimization | Savings |
|----------|---------------------|-------------------|---------|
| 1000 simple queries | $30 (all GPT-4) | $4.50 (GPT-3.5 + cache) | 85% |
| 1000 mixed queries | $50 (all GPT-4) | $15 (smart routing + cache) | 70% |
| High-traffic app (10k queries/day) | $500/day | $75/day | 85% |

## Key Metrics That Matter

Track these KPIs to ensure your optimization is working:
- **Cache hit rate**: Target 30-50% for diverse queries
- **Average cost per query**: Should be under $0.10 for 80% of requests
- **P95 latency**: 95% of queries should complete in under 5 seconds
- **Tool selection efficiency**: Average 3-5 tools selected from 20+ available
- **Model routing accuracy**: Complex queries to GPT-4 should have >90% user satisfaction

## Next Steps

1. **Add more sophisticated caching strategies** (user-specific, context-aware)
2. **Implement batch processing** for similar concurrent queries
3. **Add cost budgeting and alerts** for production safety
4. **Integrate with monitoring systems** (Prometheus, Grafana)
5. **Add A/B testing framework** for optimization experiments

## License

This code is provided for educational purposes as part of the Advanced Agentic AI Systems course.