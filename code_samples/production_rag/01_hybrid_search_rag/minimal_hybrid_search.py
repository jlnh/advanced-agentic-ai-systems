"""
Minimal Hybrid Search - Production RAG without external ML dependencies
Demonstrates core hybrid search concepts using basic implementations.
"""

import os
import numpy as np
from typing import List, Dict
from dataclasses import dataclass
from collections import Counter
import math
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class SearchResult:
    """Search result structure"""
    content: str
    score: float
    metadata: Dict
    source_type: str

class MinimalEmbeddings:
    """Simple TF-IDF based embeddings as placeholder for OpenAI embeddings"""

    def __init__(self):
        self.vocabulary = {}
        self.idf_scores = {}
        self.doc_vectors = []

    def fit_documents(self, documents: List[str]):
        """Build vocabulary and IDF scores from documents"""
        # Build vocabulary
        all_words = set()
        doc_word_counts = []

        for doc in documents:
            words = doc.lower().split()
            doc_word_counts.append(Counter(words))
            all_words.update(words)

        self.vocabulary = {word: idx for idx, word in enumerate(sorted(all_words))}

        # Calculate IDF scores
        num_docs = len(documents)
        for word in self.vocabulary:
            doc_freq = sum(1 for doc_counts in doc_word_counts if word in doc_counts)
            self.idf_scores[word] = math.log(num_docs / max(1, doc_freq))

        # Create document vectors
        self.doc_vectors = []
        for doc_counts in doc_word_counts:
            vector = np.zeros(len(self.vocabulary))
            for word, count in doc_counts.items():
                if word in self.vocabulary:
                    idx = self.vocabulary[word]
                    tf = count / sum(doc_counts.values())  # Normalize by doc length
                    vector[idx] = tf * self.idf_scores[word]

            # L2 normalize
            norm = np.linalg.norm(vector)
            if norm > 0:
                vector = vector / norm

            self.doc_vectors.append(vector)

    def embed_query(self, query: str) -> np.ndarray:
        """Convert query to vector using same vocabulary"""
        words = Counter(query.lower().split())
        vector = np.zeros(len(self.vocabulary))

        for word, count in words.items():
            if word in self.vocabulary:
                idx = self.vocabulary[word]
                tf = count / sum(words.values())
                vector[idx] = tf * self.idf_scores[word]

        # L2 normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = vector / norm

        return vector

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Find most similar documents"""
        query_vector = self.embed_query(query)

        similarities = []
        for i, doc_vector in enumerate(self.doc_vectors):
            similarity = np.dot(query_vector, doc_vector)
            similarities.append((i, 1 - similarity))  # Convert to distance

        # Sort by distance (lower is better)
        similarities.sort(key=lambda x: x[1])
        return similarities[:k]

class SimpleBM25:
    """Simple BM25 implementation"""

    def __init__(self, k1=1.5, b=0.75):
        self.k1 = k1
        self.b = b
        self.corpus = []
        self.doc_lengths = []
        self.avg_doc_length = 0
        self.doc_freqs = {}
        self.idf = {}

    def fit(self, corpus: List[str]):
        """Fit BM25 on corpus"""
        self.corpus = [doc.lower().split() for doc in corpus]
        self.doc_lengths = [len(doc) for doc in self.corpus]
        self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)

        # Calculate document frequencies
        for doc in self.corpus:
            for word in set(doc):
                self.doc_freqs[word] = self.doc_freqs.get(word, 0) + 1

        # Calculate IDF
        num_docs = len(corpus)
        for word, freq in self.doc_freqs.items():
            self.idf[word] = math.log((num_docs - freq + 0.5) / (freq + 0.5))

    def get_scores(self, query: List[str]) -> np.ndarray:
        """Get BM25 scores for query"""
        query = [word.lower() for word in query]
        scores = np.zeros(len(self.corpus))

        for i, doc in enumerate(self.corpus):
            score = 0
            for word in query:
                if word in doc:
                    tf = doc.count(word)
                    score += self.idf.get(word, 0) * (tf * (self.k1 + 1)) / (
                        tf + self.k1 * (1 - self.b + self.b * self.doc_lengths[i] / self.avg_doc_length)
                    )
            scores[i] = score

        return scores

class MinimalHybridSearch:
    """Minimal hybrid search implementation"""

    def __init__(self, semantic_weight=0.6, keyword_weight=0.4):
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight

        self.embeddings = MinimalEmbeddings()
        self.bm25 = SimpleBM25()
        self.documents = []
        self.doc_metadata = []

    def index_documents(self, documents: List[Dict]):
        """Index documents"""
        texts = [doc['content'] for doc in documents]
        self.doc_metadata = [doc['metadata'] for doc in documents]
        self.documents = texts

        print("Building minimal semantic index...")
        self.embeddings.fit_documents(texts)

        print("Building BM25 index...")
        self.bm25.fit(texts)

        print(f"Indexed {len(documents)} documents")

    def search(self, query: str, k: int = 5) -> List[SearchResult]:
        """Perform hybrid search"""
        if not self.documents:
            return []

        # Semantic search
        semantic_results = self.embeddings.similarity_search_with_score(query, k=len(self.documents))
        semantic_scores = {idx: 1 / (1 + distance) for idx, distance in semantic_results}

        # Keyword search
        bm25_scores = self.bm25.get_scores(query.split())
        max_bm25 = max(bm25_scores) if max(bm25_scores) > 0 else 1
        bm25_normalized = {i: score / max_bm25 for i, score in enumerate(bm25_scores)}

        # Combine scores
        final_results = []
        for i in range(len(self.documents)):
            semantic_score = semantic_scores.get(i, 0) * self.semantic_weight
            keyword_score = bm25_normalized.get(i, 0) * self.keyword_weight
            final_score = semantic_score + keyword_score

            if final_score > 0:
                final_results.append(SearchResult(
                    content=self.documents[i],
                    score=final_score,
                    metadata=self.doc_metadata[i],
                    source_type='hybrid'
                ))

        # Sort and return top k
        final_results.sort(key=lambda x: x.score, reverse=True)
        return final_results[:k]

def create_sample_documents():
    """Create sample documents"""
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
    """Main demonstration"""
    print("=== Minimal Hybrid Search Demo ===")
    print("This version uses simple TF-IDF and BM25 implementations")
    print("to demonstrate hybrid search concepts without external dependencies.\n")

    # Test different configurations
    configs = [
        (0.6, 0.4, "Balanced"),
        (0.4, 0.6, "Keyword-focused"),
        (0.8, 0.2, "Semantic-focused")
    ]

    documents = create_sample_documents()

    for semantic_w, keyword_w, config_name in configs:
        print(f"--- Configuration: {config_name} ---")
        print(f"Semantic weight: {semantic_w}, Keyword weight: {keyword_w}\n")

        search_engine = MinimalHybridSearch(
            semantic_weight=semantic_w,
            keyword_weight=keyword_w
        )

        search_engine.index_documents(documents)

        # Test query
        query = "Python async error handling"
        print(f"Query: '{query}'\n")

        results = search_engine.search(query, k=3)

        for i, result in enumerate(results, 1):
            print(f"  {i}. Score: {result.score:.3f}")
            print(f"     Type: {result.metadata.get('type', 'unknown')}")
            print(f"     Content: {result.content[:120]}...\n")

        print("-" * 60 + "\n")

    print("Demo completed successfully!")
    print("\nThis demonstrates the core concepts of hybrid search:")
    print("1. Semantic similarity using TF-IDF vectors")
    print("2. Keyword matching using BM25 scoring")
    print("3. Weighted combination of both approaches")
    print("4. Different weight configurations for different use cases")

if __name__ == "__main__":
    main()