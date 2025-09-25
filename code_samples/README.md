# Advanced Agentic AI Systems - Code Samples

A comprehensive collection of code samples demonstrating the implementation of advanced agentic AI systems, from basic ReAct agents to sophisticated multi-agent orchestration systems.

## Project Overview

This repository contains practical implementations of various agentic AI patterns and systems:

- **Foundations**: Core building blocks including ReAct agents, tool integration, and memory systems
- **Multi-Agent Systems**: Specialized agents and orchestration patterns
- **Advanced Concepts**: Complex workflows, optimization, and production-ready implementations

## Python Environment Setup

### Prerequisites

- Python 3.8 or higher
- Git (for cloning the repository)
- OpenAI API key (required for most examples)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd advanced-agentic-ai-systems
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

The project uses a centralized requirements system with different dependency sets:

```bash
# Install base dependencies (required for all projects)
pip install -r requirements/base.txt

# For development (includes testing and debugging tools)
pip install -r requirements/dev.txt

# For production deployments
pip install -r requirements/prod.txt
```

### 4. Environment Configuration

Most examples require environment variables for API keys and configuration:

#### Option A: Global .env file (Recommended)
Create a `.env` file in the repository root:

```bash
# OpenAI API key (required for most examples)
OPENAI_API_KEY=your_actual_openai_api_key_here

# Optional: LangChain tracing for debugging
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=your_langchain_api_key_here

# Optional: Other API keys as needed
SERP_API_KEY=your_serp_api_key_here
```

#### Option B: Export environment variables
```bash
export OPENAI_API_KEY="your-api-key-here"
export LANGCHAIN_API_KEY="your-langchain-api-key-here"
```

### 5. Verify Installation

Run the setup verification script:

```bash
python scripts/verify_phase2.py
```

This will test your environment setup and core dependencies.

## Quick Start Guide

### Running Individual Projects

Each project can be run independently. Navigate to the project directory and follow the specific instructions:

#### Foundations Projects

**Basic ReAct Agent:**
```bash
cd foundations/01_basic_react_agent
python react_agent.py
```

**Tool Integration:**
```bash
cd foundations/02_tool_integration
python research_agent.py
```

**Memory Systems:**
```bash
cd foundations/03_memory_systems
python main.py
```

#### Multi-Agent Projects

**Specialized Agents:**
```bash
cd multi_agent/01_specialized_agents
python main.py
```

### Using the Virtual Environment Consistently

For best results, always use the project's virtual environment:

```bash
# From repository root - recommended approach
./venv/bin/python path/to/specific/script.py

# Or activate and use normally
source venv/bin/activate
python path/to/specific/script.py
```

## Project Structure

```
advanced-agentic-ai-systems/
├── requirements/                    # Centralized dependency management
│   ├── base.txt                    # Core dependencies for all projects
│   ├── dev.txt                     # Development and testing tools
│   └── prod.txt                    # Production deployment dependencies
├── scripts/                        # Setup and utility scripts
│   ├── setup_project.py           # Project initialization
│   ├── verify_phase2.py           # Environment verification
│   └── test_core_components.py    # Component testing
├── src/agentic_ai/                 # Shared core components
│   ├── core/                      # Core functionality
│   │   ├── memory/               # Memory system implementations
│   │   └── orchestration/        # Agent coordination
│   └── __init__.py
├── code_samples/                   # Example implementations
│   ├── foundations/               # Foundational concepts
│   │   ├── 01_basic_react_agent/  # ReAct pattern implementation
│   │   ├── 02_tool_integration/   # Multi-tool agent system
│   │   └── 03_memory_systems/     # Memory-enhanced agents
│   └── multi_agent/              # Multi-agent systems
│       └── 01_specialized_agents/ # Agent specialization patterns
├── config/                        # Configuration files
│   └── settings.py               # Global settings
├── venv/                          # Virtual environment (after setup)
└── README.md                      # This file
```

## Common Setup Issues and Solutions

### 1. API Key Not Found
```
Error: OpenAI API key not found
```
**Solution**: Ensure `OPENAI_API_KEY` is set in your `.env` file or environment variables.

### 2. Module Import Errors
```
ModuleNotFoundError: No module named 'langchain'
```
**Solution**:
- Ensure virtual environment is activated
- Run `pip install -r requirements/base.txt`
- Verify you're using the correct Python interpreter

### 3. Permission Issues
```
PermissionError: [Errno 13] Permission denied
```
**Solution**:
- Ensure proper file permissions
- Check that output directories exist and are writable
- On Windows, run terminal as administrator if needed

### 4. Memory/FAISS Installation Issues
```
Error installing faiss-cpu
```
**Solution**:
```bash
# Try alternative installation
pip install faiss-cpu --no-cache-dir

# Or use conda if available
conda install faiss-cpu -c conda-forge
```

### 5. LangChain Hub Errors
```
Error: Missing LangChain API key
```
**Solution**: Either set `LANGCHAIN_API_KEY` in your `.env` file or use local prompts by setting `use_local_prompt=True` in agent creation.

## Development Workflow

### Setting Up for Development

1. **Install development dependencies:**
   ```bash
   pip install -r requirements/dev.txt
   ```

2. **Run tests:**
   ```bash
   python -m pytest tests/
   ```

3. **Code formatting:**
   ```bash
   black src/ code_samples/
   flake8 src/ code_samples/
   ```

### Adding New Projects

1. Create project directory under appropriate category
2. Add project-specific requirements to main requirements files
3. Include setup instructions in project README
4. Update this main README with navigation links

## Performance and Cost Optimization

### Token Management
- Most examples use `gpt-3.5-turbo` for cost efficiency
- Upgrade to `gpt-4` in config files for better performance
- Monitor token usage with verbose logging

### Caching
- Many projects include caching mechanisms
- Enable caching for repeated operations
- Clear cache regularly to manage disk space

### Rate Limiting
- Built-in rate limiting for external API calls
- Adjust limits based on your API tier
- Implement backoff strategies for production use

## Security Best Practices

- Never commit API keys to version control
- Use `.env` files for configuration (included in `.gitignore`)
- Implement input validation for user inputs
- Restrict file operations to designated directories
- Review and audit external tool integrations

## Troubleshooting Resources

### Debug Mode
Enable verbose logging for troubleshooting:

```bash
export LANGCHAIN_VERBOSE=true
export LANGCHAIN_TRACING_V2=true
python your_script.py
```

### Common Performance Issues
- **Slow responses**: Check internet connection and API status
- **High costs**: Monitor token usage and implement caching
- **Memory issues**: Clear old cache entries and optimize context windows

### Getting Help
- Check project-specific README files for detailed instructions
- Review error logs with verbose mode enabled
- Ensure all dependencies are correctly installed
- Verify API keys and permissions

## Next Steps

After setting up your environment:

1. **Start with Foundations**: Begin with `01_basic_react_agent` to understand core concepts
2. **Explore Tool Integration**: Move to `02_tool_integration` for practical applications
3. **Add Memory**: Implement memory systems with `03_memory_systems`
4. **Scale Up**: Explore multi-agent systems for complex workflows

Each project builds upon previous concepts while introducing new capabilities and patterns.

## Contributing

This is an educational project. Feel free to:
- Improve existing examples
- Add new use cases and patterns
- Enhance documentation and setup instructions
- Share optimizations and best practices

---

**Ready to build advanced agentic AI systems?** Start with the basic ReAct agent and work your way up to sophisticated multi-agent orchestration!