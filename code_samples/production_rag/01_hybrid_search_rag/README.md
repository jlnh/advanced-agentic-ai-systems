# Production RAG with Advanced Retrieval

This project implements a production-grade Retrieval-Augmented Generation (RAG) system with advanced retrieval techniques including hybrid search, re-ranking, and multi-index architecture.

**🎯 Quick Start: Use `openai_hybrid_search.py` - it's the most reliable implementation with real OpenAI embeddings and minimal dependencies.**

## Features

- **✅ Hybrid Search**: Combines semantic similarity and keyword matching for optimal retrieval accuracy
- **🔧 Multiple Implementations**: From educational concepts to production-ready systems
- **⚡ Clean Dependencies**: Working version needs only 4 packages
- **🎨 Advanced Re-Ranking**: Cross-encoder models for precise result ranking with diversity optimization
- **🏗️ Multi-Index Architecture**: Routes queries to specialized indexes based on document type
- **🔍 Query Processing**: Intelligent query routing and expansion for improved recall
- **🚀 Production Ready**: Optimized for scale with caching, batch processing, and performance monitoring

## Architecture Overview

The system consists of several key components:

1. **Hybrid Search Engine** (`hybrid_search.py`) - Combines BM25 keyword search with semantic vector search
2. **Advanced Re-Ranker** (`reranker.py`) - Uses cross-encoder models to re-rank initial results
3. **Query Router** (`query_router.py`) - Routes queries to appropriate document indexes
4. **Multi-Index RAG** (`multi_index_rag.py`) - Orchestrates the complete RAG pipeline
5. **Example Usage** (`example.py`) - Demonstrates system capabilities with sample data

## Quick Setup Guide

### 🚀 Recommended: Clean OpenAI Version (5 minutes)

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install minimal dependencies:**
```bash
pip install -r requirements-minimal.txt
```

3. **Set up API key:**
```bash
cp .env.example .env
# Edit .env file and add: OPENAI_API_KEY=your_key_here
```

4. **Run the demo:**
```bash
python openai_hybrid_search.py
```

### 📚 Alternative: No-API Version (2 minutes)

If you don't have an OpenAI API key or want to understand the concepts:

```bash
pip install numpy python-dotenv
python minimal_hybrid_search.py
```

### 🔧 Advanced: Full Features (Complex Setup)

⚠️ **Warning**: May have dependency conflicts. Only use if you need advanced features.

```bash
pip install -r requirements.txt  # or requirements-cpu.txt
python example.py  # May not work due to PyTorch/LangChain issues
```

## API Key Setup

Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys):

```bash
# Copy template
cp .env.example .env

# Edit .env file:
OPENAI_API_KEY=sk-your-actual-key-here
```

## Usage Examples

### Basic Hybrid Search (Clean Version)

```python
from openai_hybrid_search import CleanHybridSearchEngine

# Initialize search engine
search_engine = CleanHybridSearchEngine(
    semantic_weight=0.6,    # 60% semantic similarity
    keyword_weight=0.4      # 40% keyword matching
)

# Index your documents
documents = [
    {
        'content': 'Your document content here...',
        'metadata': {'type': 'technical', 'date': '2024-01-15'}
    }
]
search_engine.index_documents(documents)

# Search
results = search_engine.search("your query", k=5)
for result in results:
    print(f"Score: {result.score:.3f}")
    print(f"Content: {result.content}")
```

### Multi-Index RAG System

```python
from multi_index_rag import MultiIndexRAG
from query_router import DocumentType

# Initialize RAG system
rag_system = MultiIndexRAG()

# Index documents by type
rag_system.index_document(tech_doc, DocumentType.TECHNICAL)
rag_system.index_document(business_doc, DocumentType.BUSINESS)

# Intelligent search with routing
results = rag_system.search("Python async error handling", top_k=5)
```

## Demo Results

Here's what you'll see when running the examples:

### 🎯 OpenAI Hybrid Search Results

```
Query: 'Python async error handling'
  1. Score: 0.697 | Technical document about Python async functions ✅

Query: 'Q2 revenue growth metrics'
  1. Score: 0.744 | Business document about Q2 2024 revenue ✅

Query: 'GDPR compliance requirements'
  1. Score: 0.682 | Legal document about GDPR regulations ✅
```

### 📊 Performance Comparison

| Implementation | Accuracy | Dependencies | Setup Time | API Required |
|----------------|----------|--------------|------------|--------------|
| `openai_hybrid_search.py` | 🟢 Excellent | 4 packages | 5 min | Yes |
| `minimal_hybrid_search.py` | 🟡 Good | 2 packages | 2 min | No |
| `example.py` (LangChain) | 🔴 Has issues | 15+ packages | Complex | Yes |

### 💡 Which Version Should You Use?

- **🚀 Production/Demo**: Use `openai_hybrid_search.py` - reliable, fast, real embeddings
- **📚 Learning**: Use `minimal_hybrid_search.py` - understand concepts without API costs
- **🔬 Research**: Study the full LangChain versions for architecture patterns

### Running the Examples

**Option 1: OpenAI Version (Recommended)**
```bash
python openai_hybrid_search.py
```

**Option 2: Minimal Version (No API)**
```bash
python minimal_hybrid_search.py
```

**Option 3: Full Version (Not Recommended)**
```bash
python example.py  # May fail due to dependencies
```

## Configuration Options

### Hybrid Search Weights

Adjust semantic vs keyword search weights based on your use case:

- **Technical docs**: `semantic_weight=0.4, keyword_weight=0.6` (exact terms matter)
- **Business docs**: `semantic_weight=0.6, keyword_weight=0.4` (balanced)
- **Legal docs**: `semantic_weight=0.3, keyword_weight=0.7` (exact terminology crucial)
- **General docs**: `semantic_weight=0.8, keyword_weight=0.2` (concept-heavy)

### Re-Ranker Models

Available cross-encoder models (in order of speed vs accuracy):

- `cross-encoder/ms-marco-TinyBERT-L-2-v2` - Fastest, good for real-time
- `cross-encoder/ms-marco-MiniLM-L-6-v2` - Balanced (default)
- `cross-encoder/ms-marco-MiniLM-L-12-v2` - Slower but more accurate

### Performance Optimization

For production deployments:

1. **Enable Caching**: Query embeddings cache for 1 hour
2. **Batch Processing**: Process re-ranking in batches of 16-32
3. **Approximate Search**: Use FAISS IndexIVFFlat for >1M documents
4. **Progressive Retrieval**: Show fast results while computing refined ones

## File Structure

```
01_hybrid_search_rag/
├── README.md                      # This file
├── requirements.txt               # Full dependencies (complex, may have issues)
├── requirements-cpu.txt          # CPU-only PyTorch dependencies
├── requirements-minimal.txt      # Minimal deps for clean OpenAI version ✅
├── .env.example                  # Environment variables template
├── hybrid_search.py              # LangChain-based (dependency issues)
├── reranker.py                   # Advanced re-ranking system
├── query_router.py               # Query routing and expansion
├── multi_index_rag.py            # Multi-index orchestration
├── example.py                    # Full LangChain example (has issues)
├── simple_example.py             # Simplified example (has issues)
├── openai_hybrid_search.py      # ✅ Clean working OpenAI version
└── minimal_hybrid_search.py      # ✅ Basic version (no API required)
```

## Best Practices

### Index Optimization

- **Technical Documents**: Use smaller chunks (200-500 tokens) with code-aware splitting
- **Legal Documents**: Larger chunks (1000-2000 tokens) to preserve context
- **Business Documents**: Medium chunks (500-1000 tokens) with entity extraction

### Query Processing

- **Expand Queries**: Add synonyms and related terms for better recall
- **Route Intelligently**: Use keyword indicators to select appropriate indexes
- **Apply Filters**: Use metadata filters for date ranges, document types, access control

### Monitoring Metrics

- **Retrieval Precision@5**: Target >80% for production systems
- **Mean Reciprocal Rank**: Target >0.7 (first relevant result in top 2)
- **Query Latency P95**: Target <500ms for 95% of queries
- **Cache Hit Rate**: Query cache should achieve 20-30% hit rate

## Troubleshooting

### ✅ Common Solutions

**1. "No module named 'rank_bm25'"**
```bash
pip install rank-bm25
```

**2. "Invalid OpenAI API key"**
```bash
# Check your .env file:
cat .env
# Should show: OPENAI_API_KEY=sk-...
# Get key from: https://platform.openai.com/api-keys
```

**3. PyTorch/LangChain Dependency Issues**
```bash
# Use the clean version instead:
pip install -r requirements-minimal.txt
python openai_hybrid_search.py
```

**4. "CUDA error" or torch issues**
```bash
# Solution: Use the clean OpenAI version
python openai_hybrid_search.py  # No PyTorch required!
```

### 🚨 Known Issues & Solutions

| Issue | Affected Files | Solution |
|-------|---------------|----------|
| PyTorch CUDA conflicts | `example.py`, `simple_example.py` | Use `openai_hybrid_search.py` |
| LangChain import errors | `hybrid_search.py` | Use `openai_hybrid_search.py` |
| Heavy dependencies | `requirements.txt` | Use `requirements-minimal.txt` |
| Missing API key | All OpenAI versions | Create `.env` with valid key |

### 💡 Pro Tips

- **Start Simple**: Always try `minimal_hybrid_search.py` first
- **Production Ready**: Use `openai_hybrid_search.py` for real applications
- **Debugging**: Check the simple versions work before trying complex ones
- **API Costs**: Minimal version uses ~$0.01 for the demo

## Summary

This project provides a complete production RAG system with multiple implementation levels:

### 🎯 **Recommended Path**
1. **Start**: `python minimal_hybrid_search.py` (understand concepts)
2. **Production**: `python openai_hybrid_search.py` (real embeddings)
3. **Study**: Review full architecture files for advanced patterns

### 📈 **What You Get**
- **Working hybrid search** combining semantic + keyword matching
- **Real production examples** with OpenAI embeddings
- **Educational implementations** showing core algorithms
- **Complete documentation** with setup, usage, and troubleshooting
- **Multiple complexity levels** from basic to advanced

### 🚀 **Production Features**
- OpenAI embeddings for semantic search
- BM25 for keyword matching
- Weighted score combination
- Metadata filtering
- Clean, minimal dependencies
- Proper API key management
- Error handling and validation

The clean OpenAI version (`openai_hybrid_search.py`) is the sweet spot: production-quality results with minimal complexity. Perfect for demos, prototypes, or production systems.

---

**Ready to start?** Run `pip install -r requirements-minimal.txt && python openai_hybrid_search.py`