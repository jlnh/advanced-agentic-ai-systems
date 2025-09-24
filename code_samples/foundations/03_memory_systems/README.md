# Memory Systems for Agentic AI

This module implements a comprehensive memory system for AI agents, providing both short-term conversation context and long-term persistent learning capabilities.

## Overview

Memory systems transform stateless AI tools into intelligent assistants that learn from past conversations, remember user preferences, and build context over time. This implementation includes:

- **Short-term memory**: Manages recent conversation context with automatic summarization
- **Long-term memory**: Persistent storage using vector search for semantic retrieval
- **Memory-enhanced agent**: Combines both memory types for context-aware responses
- **Optimization tools**: Token budget management and memory compression

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Memory-Enhanced Agent System                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Current Query: "Find more quantum computing research like last time"      │
│                                       │                                     │
│                                       ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │                     Memory Management Layer                         │   │
│  │                                                                     │   │
│  │  ┌─────────────────────┐         ┌─────────────────────────────┐   │   │
│  │  │   Short-Term Memory │◄────────┤      Long-Term Memory       │   │   │
│  │  │                     │         │                             │   │   │
│  │  │ • Recent messages   │         │ • Vector store (FAISS)      │   │   │
│  │  │ • Session context   │         │ • User preferences         │   │   │
│  │  │ • Auto-summarization│         │ • Domain expertise         │   │   │
│  │  └─────────────────────┘         │ • Interaction patterns     │   │   │
│  │                                  └─────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                       │                                     │
│                                       ▼                                     │
│  Result: "I found 8 new quantum algorithm papers from 2024, similar to     │
│  the IBM and Google research you liked before..."                          │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Files Structure

```
03_memory_systems/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── main.py                     # Main example and demo script
├── short_term_memory.py        # Short-term memory implementation
├── long_term_memory.py         # Long-term vector memory implementation
├── memory_enhanced_agent.py    # Memory-enhanced agent class
├── test_memory_system.py       # Test functions and benchmarks
└── memory_store/              # Created automatically for persistent storage
    ├── index.faiss            # Vector store index
    ├── index.pkl              # Vector store metadata
    └── insights.json          # User insights and preferences
```

## Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

### 2. Run the Demo

```bash
python main.py
```

Choose from:
- **Interactive Demo**: See memory system in action with simulated conversations
- **Run Tests**: Execute comprehensive test suite
- **Both**: Run demo followed by tests

### 3. Basic Usage

```python
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from short_term_memory import ShortTermMemory
from long_term_memory import LongTermMemory
from memory_enhanced_agent import MemoryEnhancedAgent

# Initialize components
llm = OpenAI(temperature=0.7)
embeddings = OpenAIEmbeddings()

# Create memory systems
short_memory = ShortTermMemory(llm, max_token_limit=800)
long_memory = LongTermMemory(embeddings)

# Create memory-enhanced agent
memory_agent = MemoryEnhancedAgent(
    base_agent=your_base_agent,
    short_memory=short_memory,
    long_memory=long_memory
)

# Use the agent
result = memory_agent.invoke("Find research papers on quantum computing")
print(result['output'])

# End session to extract insights
summary = memory_agent.end_session()
```

## Key Features

### 🧠 Short-Term Memory
- **Conversation buffer**: Maintains recent message history
- **Auto-summarization**: Compresses old conversations to save tokens
- **Session management**: Tracks conversation sessions
- **Token optimization**: Configurable token limits

### 📚 Long-Term Memory
- **Vector storage**: FAISS-based semantic search over past interactions
- **Insight extraction**: Automatically identifies user preferences and patterns
- **Persistent storage**: Saves memory across agent restarts
- **User profiling**: Builds comprehensive user profiles over time

### 🚀 Memory-Enhanced Agent
- **Context building**: Combines short and long-term memory for rich context
- **Smart retrieval**: Finds relevant past interactions using semantic search
- **Personalization**: Uses learned preferences to customize responses
- **Error handling**: Graceful fallbacks when memory operations fail

### ⚡ Optimization Features
- **Token budget management**: Prevents context overflow
- **Memory compression**: Reduces storage size of old interactions
- **Performance monitoring**: Tracks memory usage and growth
- **Smart ranking**: Prioritizes relevant memories by recency and relevance

## Memory Types Comparison

| Memory Type | Purpose | Token Cost | Persistence | Best For |
|-------------|---------|------------|-------------|----------|
| **ConversationBuffer** | Recent context | High | Session only | Short conversations |
| **ConversationSummary** | Compressed history | Medium | Session only | Long conversations |
| **Vector Memory** | Semantic search | Low | Permanent | Learning patterns |
| **Hybrid System** | Best of both | Optimized | Both | Production systems |

## Configuration Options

### Short-Term Memory
```python
short_memory = ShortTermMemory(
    llm=llm,
    max_token_limit=1000  # Adjust based on your model's context window
)
```

### Long-Term Memory
```python
long_memory = LongTermMemory(
    embedding_model=embeddings,
    storage_path="./custom_memory_store"  # Custom storage location
)
```

### Token Optimization
```python
optimizer = TokenOptimizedMemory(max_context_tokens=1500)
optimized_context = optimizer.optimize_context(context_parts)
```

## Testing

The test suite includes:

1. **Memory Learning Test**: Verifies that the agent learns from interactions
2. **Memory Optimization Test**: Checks performance and token usage
3. **Context Retrieval Test**: Tests semantic search accuracy
4. **Session Management Test**: Validates session handling

Run tests with:
```bash
python test_memory_system.py
```

Or use the main script:
```bash
python main.py
# Choose option 2 for tests
```

## Performance Metrics

**Typical Performance:**
- Memory retrieval: <1 second
- Context building: 1-2 seconds
- Insight extraction: 2-3 seconds
- Cost reduction: 40% with smart memory vs. full history

## Best Practices

### 💡 Token Management
- Keep recent messages (last 5-10) in full detail
- Summarize old conversations to 1-2 sentences
- Store insights permanently in vector form
- Limit context to 1,500 tokens max per query

### 🔧 Production Deployment
- Use persistent storage backends (S3, databases)
- Implement regular memory backups
- Monitor memory growth and set up alerts
- Use compression for old memories

### 🛡️ Error Handling
- Graceful fallbacks when memory operations fail
- Context overflow handling for large conversations
- Memory leak prevention and monitoring

## Common Use Cases

### 🔬 Research Assistant
- Remembers research topics and preferred sources
- Learns output format preferences
- Tracks successful search strategies

### 💻 Code Helper
- Remembers programming language preferences
- Learns coding style and patterns
- Maintains project context across sessions

### 🎧 Customer Service
- Stores user history and preferences
- Remembers previous issues and resolutions
- Personalizes support based on user profile

## Troubleshooting

### Memory Store Issues
- Check file permissions in storage directory
- Ensure FAISS dependencies are installed correctly
- Verify OpenAI API key is set

### Performance Issues
- Reduce max_token_limit for short-term memory
- Implement memory compression for large stores
- Use memory monitoring to identify bottlenecks

### Context Overflow
- The system automatically handles context overflow
- Adjust token limits based on your model
- Use summarization for very long conversations

## Next Steps

After implementing memory systems, consider:

1. **Multi-agent orchestration**: Coordinate multiple agents with shared memory
2. **Specialized memory types**: Domain-specific memory patterns
3. **Real-time learning**: Continuous learning from user feedback
4. **Memory sharing**: Cross-user insights while preserving privacy

## Contributing

To extend the memory system:

1. Create new memory types by inheriting from base classes
2. Add optimization strategies in `long_term_memory.py`
3. Implement additional test cases in `test_memory_system.py`
4. Update documentation for new features

---

**Memory transforms agents from stateless tools into learning assistants that improve with every interaction!**