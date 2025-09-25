# Specialized Agents System

A demonstration of specialized AI agents working together to handle complex tasks through the power of specialization.

## Overview

This project implements three specialized agents:

- **🔍 Researcher Agent**: Specialized for information gathering and research tasks
- **📊 Analyst Agent**: Specialized for data processing, analysis, and visualization
- **✍️ Writer Agent**: Specialized for content creation and formatting

Each agent is optimized for specific tasks with carefully curated tools and prompts, following the principle that specialized agents outperform general-purpose ones.

## Project Structure

```
.
├── config.py              # Configuration and shared imports
├── researcher_agent.py     # Research specialist implementation
├── analyst_agent.py       # Data analysis specialist implementation
├── writer_agent.py        # Content writing specialist implementation
├── orchestrator.py        # Coordinates agents based on task type
├── main.py                # Demo script with example tasks
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Setup Instructions

### 1. Use Project Virtual Environment

This project is designed to work with the main project's virtual environment located at the repository root.

**Option A: Activate the virtual environment**
```bash
# Navigate to the repository root
cd path/to/advanced-agentic-ai-systems/

# Activate the virtual environment
source venv/bin/activate

# Navigate to this project directory
cd code_samples/multi_agent/01_specialized_agents/
```

**Option B: Use the virtual environment directly (recommended)**
```bash
# From the repository root directory
./venv/bin/python code_samples/multi_agent/01_specialized_agents/main.py

# Or from this project directory
../../../venv/bin/python main.py
```

### 2. Install Dependencies

```bash
# If using activated environment:
pip install -r requirements.txt

# If using direct path from repo root:
./venv/bin/pip install -r code_samples/multi_agent/01_specialized_agents/requirements.txt

# Or from this project directory:
../../../venv/bin/pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root by copying the example:

```bash
# Copy the example file
cp .env.example .env

# Edit the .env file with your actual API keys
# You can use any text editor
nano .env
```

Required environment variables in your `.env` file:

```bash
# OpenAI API key (required) - Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_actual_openai_api_key_here

# Optional: LangChain tracing for debugging
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langchain_api_key_here
```

**Important**:
- You must have a valid OpenAI API key to run this system
- Never commit your actual `.env` file to version control
- The `.env.example` file shows all available configuration options

### 4. Create Output Directory

The writer agent saves files to an outputs directory:

```bash
mkdir -p outputs
```

## How to Run

### Run the Demo

Execute the main demo script to see all three agents in action:

```bash
# Option A: If virtual environment is activated (from this directory)
python main.py

# Option B: Using direct path from repo root
./venv/bin/python code_samples/multi_agent/01_specialized_agents/main.py

# Option C: Using direct path from this directory
../../../venv/bin/python main.py
```

This will demonstrate:
1. **Research Task**: Finding latest quantum computing developments
2. **Analysis Task**: Calculating compound annual growth rate
3. **Writing Task**: Creating an executive summary

### Use Individual Agents

You can also import and use individual agents:

```python
from orchestrator import SpecializedAgentSystem

# Initialize the system
system = SpecializedAgentSystem()

# Execute a specific task
result = system.execute("Research the latest AI developments")
print(result)
```

### Direct Agent Usage

For more control, use agents directly:

```python
from researcher_agent import create_researcher_agent

# Create a specific agent
researcher = create_researcher_agent()

# Use it directly
result = researcher.invoke({
    "input": "Find information about quantum computing breakthroughs"
})
```

## Agent Capabilities

### 🔍 Researcher Agent
- **Tools**: Web search, news search
- **Strengths**: Finding current information, fact verification, source citation
- **Use Cases**: Market research, competitive analysis, current events

### 📊 Analyst Agent
- **Tools**: Python REPL, statistical calculations
- **Strengths**: Data processing, pattern recognition, visualization
- **Use Cases**: Financial analysis, performance metrics, trend identification

### ✍️ Writer Agent
- **Tools**: File writing, markdown formatting, summarization
- **Strengths**: Content creation, formatting, audience adaptation
- **Use Cases**: Reports, documentation, executive summaries

## Configuration Options

### Modify LLM Settings

Edit `config.py` to change the language model:

```python
llm = ChatOpenAI(
    model="gpt-4",  # Upgrade for better performance
    temperature=0.1,  # Adjust creativity
    max_tokens=3000   # Increase for longer responses
)
```

### Add New Tools

Extend any agent by adding tools to their respective files:

```python
# In researcher_agent.py
new_tool = Tool(
    name="custom_search",
    func=your_custom_function,
    description="Description of what this tool does"
)

research_tools.append(new_tool)
```

## Troubleshooting

### Common Issues

1. **Missing OpenAI API Key**
   ```
   Error: OpenAI API key not found
   Solution: Set OPENAI_API_KEY in your .env file
   ```

2. **Import Errors**
   ```
   Error: ModuleNotFoundError
   Solution: Ensure virtual environment is activated and dependencies installed
   ```

3. **Permission Errors**
   ```
   Error: Permission denied when writing files
   Solution: Ensure outputs directory exists and is writable
   ```

### Debug Mode

Enable verbose logging by setting environment variable:

```bash
# Option A: If virtual environment is activated (from this directory)
export LANGCHAIN_VERBOSE=true
python main.py

# Option B: Using direct path from repo root
LANGCHAIN_VERBOSE=true ./venv/bin/python code_samples/multi_agent/01_specialized_agents/main.py

# Option C: Using direct path from this directory
LANGCHAIN_VERBOSE=true ../../../venv/bin/python main.py
```

### Cost Management

- The system uses `gpt-3.5-turbo` by default for cost efficiency
- Monitor token usage in verbose mode
- Set `max_iterations` limits on agents to prevent runaway costs

## Architecture Principles

This implementation follows these design principles:

- **Single Responsibility**: Each agent has a clear, focused role
- **Tool Minimization**: Agents only have tools necessary for their specialty
- **Graceful Degradation**: Proper error handling when tasks are out of scope
- **Clear Interfaces**: Well-defined inputs and outputs between components

## Next Steps

To extend this system:

1. **Add New Specialists**: Create agents for specific domains (legal, medical, etc.)
2. **Improve Classification**: Use embeddings or LLM-based task routing
3. **Add Workflows**: Chain agents together for complex multi-step processes
4. **Add Monitoring**: Implement metrics tracking and performance monitoring
5. **Production Hardening**: Add authentication, rate limiting, and scaling capabilities

## License

This code is provided for educational purposes as part of the Advanced Agentic AI Systems course.