# Basic ReAct Agent - Module 1 Task 1

A foundational implementation of the ReAct (Reasoning and Acting) pattern using LangChain. This agent demonstrates how AI can think step-by-step and take actions to solve problems.

## 🎯 What is ReAct?

The ReAct pattern enables AI agents to:
- **Think** step-by-step about problems
- **Act** by using tools (Python, web search, file operations)
- **Observe** results and continue reasoning

**Pattern Flow:** Thought → Action → Observation → repeat until done

## 🏗️ Architecture

```
User Query → LLM Reasoning → Agent Executor → Tools → Results
     ↑                                              ↓
     ←──────── Final Answer ←─────── Observation ←───
```

## 📁 Project Structure

```
01_basic_react_agent/
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── react_agent.py     # Main ReAct agent implementation
├── test_agent.py      # Test suite with examples
└── debug_utils.py     # Debugging tools and utilities
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
```bash
# Option 1: Environment variable
export OPENAI_API_KEY="your-api-key-here"

# Option 2: Or set in code (not recommended for production)
# Edit react_agent.py and uncomment the line in setup_environment()
```

### 3. Run Basic Agent
```bash
python react_agent.py
```

### 4. Run Comprehensive Tests
```bash
python test_agent.py
```

## 📚 File Descriptions

### `react_agent.py`
Core ReAct agent implementation with:
- Environment setup
- Basic agent creation with GPT-4 and Python REPL
- Error handling and retry logic
- Simple test execution

### `test_agent.py`
Interactive test suite featuring:
- **Basic Tests**: Simple verification (2+2, square root)
- **Progressive Tests**: Increasing complexity
  - Simple arithmetic (25% of 1,380)
  - Financial calculations (compound interest)
  - Data analysis (prime number summation)

### `debug_utils.py`
Debugging utilities including:
- Enhanced debugging output
- Custom tool creation examples
- Custom prompt templates
- Execution tracing tools

## 🎮 Usage Examples

### Basic Usage
```python
from react_agent import create_basic_agent, robust_agent_call

# Create agent
agent = create_basic_agent()

# Ask a question
result = robust_agent_call(agent, "What is 25% of 1,380?")
print(result['output'])  # Output: 345
```

### With Debugging
```python
from debug_utils import create_debugging_agent, debug_agent_execution

# Create debugging agent
agent = create_debugging_agent()

# Execute with detailed output
debug_agent_execution(agent, "Calculate compound interest on $1000 at 5% for 3 years")
```

### Running Tests Interactively
```bash
python test_agent.py
# Choose:
# 1. Basic tests (quick verification)
# 2. Progressive tests (increasing complexity)
# 3. Both
```

## 🔧 Configuration Options

### Agent Parameters
```python
ChatOpenAI(
    model="gpt-4",        # Model choice (gpt-4, gpt-3.5-turbo)
    temperature=0         # 0 = deterministic, 1 = creative
)

AgentExecutor(
    max_iterations=5,     # Prevent infinite loops
    verbose=True         # Show reasoning process
)
```

### Available Tools
- **PythonREPLTool**: Execute Python code for calculations
- Easily extensible with web search, file operations, etc.

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
   ```
   Error: OpenAI API key not found
   ```
   **Solution**: Set `OPENAI_API_KEY` environment variable

2. **Import Error**
   ```
   ModuleNotFoundError: No module named 'langchain'
   ```
   **Solution**: Run `pip install -r requirements.txt`

3. **Agent Gets Stuck**
   ```
   Agent exceeded max iterations
   ```
   **Solution**: Increase `max_iterations` or simplify query

4. **Tool Selection Issues**
   - Agent chooses wrong tools or fails to use tools
   - **Solution**: Use clearer tool descriptions (see `debug_utils.py`)

### Debug Mode
Always use `verbose=True` during development to see the agent's reasoning process:

```python
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True  # Shows thought process
)
```

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Execution Time** | 5-15s (simple), 30-60s (complex) |
| **Cost** | ~$0.01-0.05 per query (GPT-4) |
| **Success Rate** | 90%+ (well-defined problems) |
| **Supported Tasks** | Math, logic, basic data analysis |

## 🎯 Example Queries to Try

### Simple
- "What is 2+2?"
- "Calculate the square root of 144"
- "What is 15% of 200?"

### Intermediate
- "Calculate compound interest on $5000 at 3% for 5 years"
- "Find the factorial of 10"
- "Convert 100 degrees Fahrenheit to Celsius"

### Advanced
- "Generate first 20 Fibonacci numbers and find their sum"
- "Create a list of prime numbers under 100 and calculate their average"
- "Solve the quadratic equation x² - 5x + 6 = 0"

## 🔄 Next Steps

This basic agent can be extended with:
- **Web Search**: Add search capabilities
- **File Operations**: Read/write files
- **Database Access**: Query databases
- **API Integration**: Connect to external services
- **Custom Tools**: Domain-specific functionality

## 📖 Learning Resources

- [LangChain Documentation](https://docs.langchain.com/)
- [ReAct Paper](https://arxiv.org/abs/2210.03629)
- [Agent Patterns Guide](https://docs.langchain.com/docs/use-cases/agents)

## 🤝 Contributing

This is an educational project. Feel free to:
- Add new test cases
- Improve error handling
- Create additional tools
- Enhance debugging utilities

---

**Ready to build your first ReAct agent?** Start with `python react_agent.py` and explore the reasoning process!