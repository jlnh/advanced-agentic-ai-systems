# Multi-Tool Research Agent

A comprehensive AI agent system that integrates multiple tools for web search, file management, data analysis, and report generation. This implementation demonstrates how to build production-ready AI agents that can interact with real-world systems.

## Overview

This project implements a multi-tool research assistant that can:
- Search the web and Wikipedia for information
- Analyze and process research data
- Format findings into professional reports
- Manage files and workspace operations
- Monitor tool usage and performance
- Implement security best practices

## Architecture

The system consists of several modular components:

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Multi-Tool Agent Architecture                     │
├─────────────────────────────────────────────────────────────────────┤
│  User Query → Agent Executor → Tool Selection → Result Processing   │
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐           │
│  │    Web      │  │    File     │  │     Custom      │           │
│  │   Search    │  │ Operations  │  │   Business      │           │
│  │   Tools     │  │    Tools    │  │    Tools        │           │
│  └─────────────┘  └─────────────┘  └─────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
├── research_agent.py      # Main agent implementation and testing
├── tool_setup.py          # Web search and file management tools
├── custom_tools.py        # Business logic and analysis tools
├── monitoring.py          # Usage tracking and performance monitoring
├── security_utils.py      # Security validation and workspace setup
├── performance_utils.py   # Caching and optimization utilities
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Environment Variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   ```

3. **Create Workspace Directory**
   ```bash
   mkdir agent_workspace
   ```

## Quick Start

### Basic Usage

```python
from research_agent import create_research_agent

# Create the agent
agent = create_research_agent()

# Run a simple search and save
result = agent.invoke({
    "input": "Search for recent AI developments and save to 'ai_trends.md'"
})
```

### Advanced Research Workflow

```python
# Complex multi-step research
result = agent.invoke({
    "input": """
    Research quantum computing breakthroughs in 2024,
    analyze the key trends and implications,
    format as a professional report,
    and save to 'quantum_report.md'
    """
})
```

## Available Tools

### Search Tools
- **Web Search**: DuckDuckGo search for current information
- **Wikipedia**: Reliable reference information lookup

### File Management
- **Save File**: Store research findings and reports
- **Read File**: Access previously saved content
- **List Files**: Browse workspace directory

### Analysis Tools
- **Data Analyzer**: Extract insights from research data
- **Report Formatter**: Structure content into professional reports

## Key Features

### 🔍 **Intelligent Tool Selection**
The agent automatically chooses the best tools for each task based on context and requirements.

### 📁 **Secure File Operations**
All file operations are restricted to a secure workspace directory with input validation.

### 🔧 **Custom Business Logic**
Easily extensible framework for adding domain-specific tools and analysis functions.

### 📊 **Performance Monitoring**
Built-in tracking for tool usage, success rates, and execution times.

### 🛡️ **Security Best Practices**
- Input validation and sanitization
- Rate limiting for external APIs
- Secure workspace directory permissions
- Protection against directory traversal attacks

## Testing

Run the built-in tests to verify functionality:

```python
python research_agent.py
```

This will execute three test scenarios:
1. Simple web search and file save
2. Complex research workflow with analysis
3. File management operations

## Configuration

### Tool Priorities
Modify tool selection behavior in `performance_utils.py`:

```python
TOOL_PRIORITIES = {
    "file_operations": 1,    # Fastest, free
    "wikipedia": 2,          # Fast, free
    "web_search": 3,         # Moderate speed, free
    "custom_api": 4          # Varies by API
}
```

### Rate Limiting
Control API usage in `monitoring.py`:

```python
@rate_limit(calls_per_minute=20)
def controlled_search(query):
    return search_tool.run(query)
```

### Security Settings
Adjust security parameters in `security_utils.py`:

```python
allowed_extensions = [".txt", ".md", ".json", ".csv"]
max_input_length = 10000
```

## Performance Optimization

### Caching
Enable result caching for expensive operations:

```python
from performance_utils import cached_web_search
result = cached_web_search("your query")
```

### Batch Operations
Process multiple files efficiently:

```python
from performance_utils import batch_file_operations
results = batch_file_operations(["file1.md", "file2.md"], read_tool)
```

## Error Handling

The system includes robust error handling:
- Graceful degradation when tools fail
- Retry logic for transient failures
- Detailed error logging and reporting
- Fallback strategies for critical operations

## Extension Points

### Adding New Tools
1. Create tool function in `custom_tools.py`
2. Wrap with LangChain `Tool` class
3. Add to tool list in `research_agent.py`

### Custom Analysis Logic
Modify `analyze_search_results()` in `custom_tools.py` to implement your business logic.

### Security Policies
Update validation rules in `security_utils.py` for your specific requirements.

## Best Practices

1. **Always validate inputs** before processing
2. **Use rate limiting** for external API calls
3. **Monitor tool performance** to identify bottlenecks
4. **Cache expensive operations** when possible
5. **Implement proper error handling** for production use

## Troubleshooting

### Common Issues

**Tool Selection Problems**: Improve tool descriptions for better agent decision-making
**File Permission Errors**: Ensure workspace directory has proper permissions
**API Rate Limits**: Implement appropriate rate limiting and caching
**Memory Usage**: Clear expired cache entries regularly

### Performance Tips

- File operations: <1 second
- Web search: 2-5 seconds
- Custom analysis: 1-3 seconds
- Full workflow: 10-30 seconds

## Security Considerations

This implementation includes several security measures:
- Input validation to prevent injection attacks
- File operation restrictions to prevent directory traversal
- Rate limiting to prevent API abuse
- Secure workspace with controlled permissions

Always review and test security measures before deploying in production environments.

## License

This project is provided for educational purposes. Review and adapt security measures for production use.