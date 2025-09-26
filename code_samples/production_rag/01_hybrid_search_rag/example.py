"""
Example Usage - Production RAG with Advanced Retrieval
Demonstrates how to use the hybrid search system with sample data.
"""

import os
from dotenv import load_dotenv
from hybrid_search import HybridSearchEngine, SearchResult
from multi_index_rag import MultiIndexRAG
from query_router import DocumentType

# Load environment variables
load_dotenv()

def create_sample_documents():
    """Create sample documents for demonstration"""
    return [
        {
            'content': 'Python async functions allow for asynchronous programming. '
                      'Use async def to define an async function and await to call it. '
                      'Common errors include forgetting await keyword or mixing sync/async code.',
            'metadata': {'type': 'technical', 'language': 'python', 'date': '2024-01-15'}
        },
        {
            'content': 'Revenue for Q2 2024 showed 15% growth over previous quarter. '
                      'Customer acquisition cost decreased by 8% while retention improved. '
                      'Market expansion strategy shows promising ROI metrics.',
            'metadata': {'type': 'business', 'quarter': 'Q2', 'year': '2024'}
        },
        {
            'content': 'The service agreement clause 3.2 states liability limitations. '
                      'Compliance with GDPR regulations requires explicit consent. '
                      'Contract terms must be reviewed quarterly for policy updates.',
            'metadata': {'type': 'legal', 'section': '3.2', 'regulation': 'GDPR'}
        },
        {
            'content': 'Machine learning models require careful evaluation metrics. '
                      'Cross-validation helps prevent overfitting. Performance should be '
                      'measured using appropriate metrics like F1-score for classification.',
            'metadata': {'type': 'general', 'topic': 'machine learning'}
        }
    ]

def demo_hybrid_search():
    """Demonstrate basic hybrid search functionality"""
    print("=== Hybrid Search Demo ===")

    # Initialize hybrid search engine
    search_engine = HybridSearchEngine(
        semantic_weight=0.6,
        keyword_weight=0.4
    )

    # Create and index sample documents
    documents = create_sample_documents()
    search_engine.index_documents(documents)

    # Test search queries
    queries = [
        "Python async error handling",
        "Q2 revenue growth metrics",
        "GDPR compliance requirements"
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")
        results = search_engine.search(query, k=3)

        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result.score:.3f} | Source: {result.source_type}")
            print(f"     Content: {result.content[:100]}...")
            print(f"     Metadata: {result.metadata}")

def demo_multi_index_rag():
    """Demonstrate multi-index RAG system"""
    print("\n\n=== Multi-Index RAG Demo ===")

    # Initialize multi-index RAG
    rag_system = MultiIndexRAG()

    # Index documents by type
    documents = create_sample_documents()

    for doc in documents:
        if doc['metadata']['type'] == 'technical':
            rag_system.index_document(doc, DocumentType.TECHNICAL)
        elif doc['metadata']['type'] == 'business':
            rag_system.index_document(doc, DocumentType.BUSINESS)
        elif doc['metadata']['type'] == 'legal':
            rag_system.index_document(doc, DocumentType.LEGAL)
        else:
            rag_system.index_document(doc, DocumentType.GENERAL)

    # Test intelligent routing
    queries = [
        "How to handle async function errors in Python?",
        "What was the revenue growth in Q2 2024?",
        "GDPR compliance policy requirements"
    ]

    for query in queries:
        print(f"\nQuery: '{query}'")

        # Show routing decision
        target_indexes = rag_system.router.route_query(query)
        print(f"Routing to indexes: {[idx.value for idx in target_indexes]}")

        # Get results
        results = rag_system.search(query, top_k=2)

        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result.score:.3f}")
            print(f"     Index: {result.metadata.get('index_type', 'unknown')}")
            print(f"     Content: {result.content[:150]}...")

def main():
    """Main demonstration function"""
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return

    try:
        # Run demonstrations
        demo_hybrid_search()
        demo_multi_index_rag()

        print("\n=== Demo Complete ===")
        print("The system successfully demonstrated:")
        print("1. Hybrid search combining semantic + keyword matching")
        print("2. Multi-index architecture with intelligent query routing")
        print("3. Advanced re-ranking for improved result quality")

    except Exception as e:
        print(f"Error running demo: {e}")
        print("Please ensure all dependencies are installed and API key is valid.")

if __name__ == "__main__":
    main()