"""
Simple Example - Production RAG with Advanced Retrieval
Demonstrates hybrid search without re-ranking to avoid CUDA issues.
"""

import os
from dotenv import load_dotenv
from hybrid_search import HybridSearchEngine

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
    print("=== Hybrid Search Demo (without re-ranking) ===")

    # Initialize hybrid search engine with different configurations
    configs = [
        (0.6, 0.4, "Balanced"),
        (0.4, 0.6, "Keyword-focused"),
        (0.8, 0.2, "Semantic-focused")
    ]

    documents = create_sample_documents()

    for semantic_w, keyword_w, config_name in configs:
        print(f"\n--- Configuration: {config_name} (semantic: {semantic_w}, keyword: {keyword_w}) ---")

        search_engine = HybridSearchEngine(
            semantic_weight=semantic_w,
            keyword_weight=keyword_w
        )

        # Index documents
        search_engine.index_documents(documents)

        # Test search queries
        query = "Python async error handling"
        print(f"\nQuery: '{query}'")
        results = search_engine.search(query, k=2)

        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result.score:.3f} | Source: {result.source_type}")
            print(f"     Content: {result.content[:100]}...")

def demo_query_routing():
    """Demonstrate query routing without the full multi-index system"""
    print("\n\n=== Query Routing Demo ===")

    from query_router import QueryRouter

    router = QueryRouter()

    test_queries = [
        "Python async function error debugging",
        "Q2 revenue growth business metrics",
        "GDPR compliance legal requirements",
        "general information about topics"
    ]

    for query in test_queries:
        target_indexes = router.route_query(query)
        print(f"Query: '{query}'")
        print(f"  -> Routes to: {[idx.value for idx in target_indexes]}")

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
        demo_query_routing()

        print("\n=== Demo Complete ===")
        print("The system successfully demonstrated:")
        print("1. Hybrid search with different weight configurations")
        print("2. Query routing to appropriate document types")
        print("3. Semantic + keyword search combination")
        print("\nNote: Re-ranking demo skipped to avoid CUDA compatibility issues.")

    except Exception as e:
        print(f"Error running demo: {e}")
        print("Please ensure all dependencies are installed and API key is valid.")

if __name__ == "__main__":
    main()