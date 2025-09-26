# Advanced Agentic AI Systems

A comprehensive collection of code samples and implementations demonstrating advanced agentic AI patterns, from basic ReAct agents to sophisticated multi-agent orchestration systems and production deployments.

**New to agentic AI systems?** 📖 [Read our comprehensive introduction](docs/introduction.md) to understand the concepts and architecture behind autonomous AI systems.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- OpenAI API key (required for most examples)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd advanced-agentic-ai-systems

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/base.txt
```

### 2. Environment Configuration
Create a `.env` file in the repository root:
```bash
# Required for most examples
OPENAI_API_KEY=your_actual_openai_api_key_here

# Optional: LangChain tracing for debugging
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

## 💻 Code Samples - Practical Implementations

### Quick Start Guide

Each project can be run independently. Navigate to the project directory and follow these instructions:

#### Foundations Projects

**Basic ReAct Agent:**
```bash
cd code_samples/foundations/01_basic_react_agent
python react_agent.py
```

**Tool Integration:**
```bash
cd code_samples/foundations/02_tool_integration
python research_agent.py
```

**Memory Systems:**
```bash
cd code_samples/foundations/03_memory_systems
python main.py
```

#### Multi-Agent Projects

**Specialized Agents:**
```bash
cd code_samples/multi_agent/01_specialized_agents
python main.py
```

**Orchestration System:**
```bash
cd code_samples/multi_agent/02_orchestration
python quick_test.py  # No API calls required
python orchestration_example.py  # Full example with API
```

**Performance Optimization:**
```bash
cd code_samples/multi_agent/03_performance_optimization
python simple_demo.py  # No API calls required
python example_usage.py  # Full example with API
```

#### Production RAG Projects

**Hybrid Search RAG:**
```bash
cd code_samples/production_rag/01_hybrid_search_rag
python minimal_hybrid_search.py  # No API required
python openai_hybrid_search.py  # With OpenAI API
```

**Caching Optimization:**
```bash
cd code_samples/production_rag/02_caching_optimization
python test_without_api.py  # No API calls required
python cost_optimized_agent.py  # Full example with API
```

#### Deployment Projects

**Observability:**
```bash
cd code_samples/deployment/01_observability
python observability_setup.py
```

**Production API:**
```bash
cd code_samples/deployment/02_production_api
docker-compose up --build
```

### Project Structure

```
code_samples/
├── foundations/                    # Foundational concepts
│   ├── 01_basic_react_agent/      # ReAct pattern implementation
│   ├── 02_tool_integration/       # Multi-tool agent system
│   └── 03_memory_systems/         # Memory-enhanced agents
├── multi_agent/                   # Multi-agent systems
│   ├── 01_specialized_agents/     # Agent specialization patterns
│   ├── 02_orchestration/          # Multi-agent orchestration
│   └── 03_performance_optimization/ # Performance optimization
├── production_rag/                # Production RAG systems
│   ├── 01_hybrid_search_rag/      # Advanced retrieval systems
│   └── 02_caching_optimization/   # Intelligent caching
└── deployment/                    # Production deployment
    ├── 01_observability/          # Monitoring and observability
    └── 02_production_api/         # Production API
```

## 📖 Projects Overview

### 🔰 Foundations
- **01_basic_react_agent** - ReAct pattern implementation with GPT-4 and Python tools
- **02_tool_integration** - Multi-tool research agent with web search and file operations
- **03_memory_systems** - Short-term and long-term memory systems for AI agents

### 🤝 Multi-Agent Systems
- **01_specialized_agents** - Researcher, Analyst, and Writer agents working together
- **02_orchestration** - Supervisor-coordinated multi-agent system with dependency management
- **03_performance_optimization** - Production-ready system with parallel execution and caching

### 🔍 Production RAG
- **01_hybrid_search_rag** - Semantic + keyword search with re-ranking
- **02_caching_optimization** - Intelligent caching and cost optimization strategies

### 🚀 Deployment
- **01_observability** - LangSmith integration with monitoring and evaluation
- **02_production_api** - FastAPI application with authentication and rate limiting

## 🎯 Learning Path Recommendations

### Beginner Path
1. `foundations/01_basic_react_agent` - Understand ReAct pattern
2. `foundations/02_tool_integration` - Learn tool integration
3. `multi_agent/01_specialized_agents` - Explore agent specialization

### Intermediate Path
1. `foundations/03_memory_systems` - Add memory capabilities
2. `multi_agent/02_orchestration` - Learn coordination patterns
3. `production_rag/01_hybrid_search_rag` - Implement advanced retrieval

### Advanced Path
1. `multi_agent/03_performance_optimization` - Master optimization
2. `production_rag/02_caching_optimization` - Implement cost optimization
3. `deployment/01_observability` - Add monitoring
4. `deployment/02_production_api` - Deploy to production

📖 **Need more details?** See our comprehensive guides:
- [Production Setup Guide](docs/production-setup.md) - Repository structure and deployment
- [Performance Metrics](docs/performance-metrics.md) - Benchmarks and optimization results
- [Troubleshooting Guide](docs/troubleshooting.md) - Common issues and solutions

## 🤝 Contributing

This is an educational project. Feel free to:
- Improve existing examples
- Add new use cases and patterns
- Enhance documentation and setup instructions
- Share optimizations and best practices

## 📚 Additional Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Multi-Agent System Design Patterns](https://en.wikipedia.org/wiki/Multi-agent_system)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)

---

**Ready to build advanced agentic AI systems?** Start with the basic ReAct agent and work your way up to sophisticated multi-agent orchestration and production deployment!