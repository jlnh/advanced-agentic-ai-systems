"""
Hybrid Search Engine - Production RAG with Advanced Retrieval
Combines semantic and keyword search for optimal retrieval accuracy.
"""

import os
from typing import List, Dict, Tuple
import numpy as np
from rank_bm25 import BM25Okapi
from langchain_community.vectorstores import FAISS
from langchain_openai.embeddings import OpenAIEmbeddings
from dataclasses import dataclass
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

class HybridSearchEngine:
    """Production-grade hybrid search combining semantic and keyword search"""

    def __init__(self,
                 semantic_weight: float = 0.6,
                 keyword_weight: float = 0.4):
        """
        Initialize hybrid search with configurable weights.
        Weights should sum to 1.0 for normalized scores.
        """
        self.semantic_weight = semantic_weight
        self.keyword_weight = keyword_weight

        # Semantic search components
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.vector_store = None

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
        print("Building semantic index...")
        self.vector_store = FAISS.from_texts(
            texts=texts,
            embedding=self.embeddings,
            metadatas=metadatas
        )

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
        Returns unified, re-scored results.
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

        # Use metadata filtering if provided
        search_kwargs = {"k": k}
        if filter_dict:
            search_kwargs["filter"] = filter_dict

        results = self.vector_store.similarity_search_with_score(
            query,
            **search_kwargs
        )

        return [
            SearchResult(
                content=doc.page_content,
                score=float(1 / (1 + score)),  # Convert distance to similarity
                metadata=doc.metadata,
                source_type='semantic'
            )
            for doc, score in results
        ]

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