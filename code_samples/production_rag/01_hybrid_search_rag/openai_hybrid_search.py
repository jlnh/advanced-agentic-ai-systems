"""
OpenAI-based Hybrid Search - Clean implementation without LangChain dependencies
Uses direct OpenAI API calls for embeddings to avoid PyTorch/transformers conflicts.
"""

import os
import numpy as np
from typing import List, Dict
from dataclasses import dataclass
from rank_bm25 import BM25Okapi
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class SearchResult:
    """Unified search result structure"""
    content: str
    score: float
    metadata: Dict
    source_type: str  # 'semantic' or 'keyword'

class OpenAIEmbeddings:
    """Direct OpenAI API embeddings client"""

    def __init__(self, api_key: str = None, model: str = "text-embedding-3-small"):
        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.model = model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for multiple documents"""
        response = self.client.embeddings.create(
            model=self.model,
            input=texts
        )
        return [data.embedding for data in response.data]

    def embed_query(self, text: str) -> List[float]:
        """Get embedding for a single query"""
        response = self.client.embeddings.create(
            model=self.model,
            input=[text]
        )
        return response.data[0].embedding

class SimpleVectorStore:
    """Simple vector store using cosine similarity"""

    def __init__(self, embeddings_client: OpenAIEmbeddings):
        self.embeddings_client = embeddings_client
        self.vectors = []
        self.texts = []
        self.metadatas = []

    def add_texts(self, texts: List[str], metadatas: List[Dict] = None):
        """Add texts to the vector store"""
        print("Getting embeddings from OpenAI...")
        embeddings = self.embeddings_client.embed_documents(texts)

        self.vectors.extend(embeddings)
        self.texts.extend(texts)
        if metadatas:
            self.metadatas.extend(metadatas)
        else:
            self.metadatas.extend([{}] * len(texts))

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Find most similar documents with scores"""
        if not self.vectors:
            return []

        query_embedding = self.embeddings_client.embed_query(query)

        # Calculate cosine similarities
        similarities = []
        for i, doc_embedding in enumerate(self.vectors):
            # Cosine similarity
            dot_product = np.dot(query_embedding, doc_embedding)
            norm_query = np.linalg.norm(query_embedding)
            norm_doc = np.linalg.norm(doc_embedding)
            similarity = dot_product / (norm_query * norm_doc)

            # Convert to distance (lower is better for compatibility)
            distance = 1 - similarity
            similarities.append((i, distance))

        # Sort by distance (lower is better)
        similarities.sort(key=lambda x: x[1])
        return similarities[:k]

class CleanHybridSearchEngine:
    """Production-grade hybrid search without heavy dependencies"""

    def __init__(self,
                 semantic_weight: float = 0.6,
                 keyword_weight: float = 0.4,
                 api_key: str = None):
        """
        Initialize hybrid search with configurable weights.
        """
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight

        # Semantic search components
        self.embeddings = OpenAIEmbeddings(api_key=api_key)
        self.vector_store = SimpleVectorStore(self.embeddings)

        # Keyword search components
        self.bm25 = None
        self.documents = []
        self.doc_metadata = []

    def index_documents(self, documents: List[Dict]):
        """Index documents for both semantic and keyword search"""

        # Extract text and metadata
        texts = [doc['content'] for doc in documents]
        metadatas = [doc['metadata'] for doc in documents]

        # Build semantic index
        print("Building semantic index with OpenAI embeddings...")
        self.vector_store.add_texts(texts, metadatas)

        # Build keyword index (BM25)
        print("Building keyword index...")
        tokenized_docs = [doc.lower().split() for doc in texts]
        self.bm25 = BM25Okapi(tokenized_docs)
        self.documents = texts
        self.doc_metadata = metadatas

        print(f"Indexed {len(documents)} documents for hybrid search")

    def search(self,
               query: str,
               k: int = 20,
               filter_dict: Dict = None) -> List[SearchResult]:
        """
        Perform hybrid search combining semantic and keyword results.
        """

        # Semantic search
        semantic_results = self._semantic_search(query, k * 2, filter_dict)

        # Keyword search
        keyword_results = self._keyword_search(query, k * 2)

        # Combine and re-rank
        combined_results = self._combine_results(
            semantic_results,
            keyword_results,
            k
        )

        return combined_results

    def _semantic_search(self,
                         query: str,
                         k: int,
                         filter_dict: Dict = None) -> List[SearchResult]:
        """Perform semantic similarity search"""

        results = self.vector_store.similarity_search_with_score(query, k=k)

        search_results = []
        for idx, distance in results:
            # Apply metadata filtering if provided
            if filter_dict:
                metadata = self.vector_store.metadatas[idx]
                if not all(metadata.get(key) == value for key, value in filter_dict.items()):
                    continue

            search_results.append(SearchResult(
                content=self.vector_store.texts[idx],
                score=float(1 / (1 + distance)),  # Convert distance to similarity
                metadata=self.vector_store.metadatas[idx],
                source_type='semantic'
            ))

        return search_results

    def _keyword_search(self, query: str, k: int) -> List[SearchResult]:
        """Perform BM25 keyword search"""

        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        # Get top k indices
        top_indices = np.argsort(scores)[::-1][:k]

        results = []
        for idx in top_indices:
            if scores[idx] > 0:  # Only include non-zero scores
                results.append(SearchResult(
                    content=self.documents[idx],
                    score=float(scores[idx] / (scores[idx] + 1)),  # Normalize
                    metadata=self.doc_metadata[idx],
                    source_type='keyword'
                ))

        return results

    def _combine_results(self,
                        semantic_results: List[SearchResult],
                        keyword_results: List[SearchResult],
                        k: int) -> List[SearchResult]:
        """Combine and re-score results using weighted fusion"""

        # Create a unified score dictionary
        combined_scores = {}

        # Add semantic scores
        for result in semantic_results:
            key = result.content[:100]  # Use first 100 chars as key
            combined_scores[key] = {
                'content': result.content,
                'metadata': result.metadata,
                'semantic_score': result.score * self.semantic_weight,
                'keyword_score': 0
            }

        # Add keyword scores
        for result in keyword_results:
            key = result.content[:100]
            if key in combined_scores:
                combined_scores[key]['keyword_score'] = (
                    result.score * self.keyword_weight
                )
            else:
                combined_scores[key] = {
                    'content': result.content,
                    'metadata': result.metadata,
                    'semantic_score': 0,
                    'keyword_score': result.score * self.keyword_weight
                }

        # Calculate final scores and sort
        final_results = []
        for key, data in combined_scores.items():
            final_score = data['semantic_score'] + data['keyword_score']
            final_results.append(SearchResult(
                content=data['content'],
                score=final_score,
                metadata=data['metadata'],
                source_type='hybrid'
            ))

        # Sort by score and return top k
        final_results.sort(key=lambda x: x.score, reverse=True)
        return final_results[:k]

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

def main():
    """Main demonstration function"""
    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found in environment variables.")
        print("Please create a .env file with your OpenAI API key.")
        return

    try:
        print("=== Clean Hybrid Search Demo (OpenAI API) ===")

        # Initialize hybrid search engine
        search_engine = CleanHybridSearchEngine(
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

        print("\n=== Demo Complete ===")
        print("Successfully demonstrated:")
        print("1. OpenAI embeddings-based semantic search")
        print("2. BM25 keyword search")
        print("3. Hybrid search with weighted combination")

    except Exception as e:
        print(f"Error running demo: {e}")
        print("Please ensure your OpenAI API key is valid and has credits.")

if __name__ == "__main__":
    main()