"""
Advanced Re-Ranker - Production RAG Component
Uses cross-encoder models for precise ranking with diversity optimization.
"""

from sentence_transformers import CrossEncoder
import torch
import numpy as np
from typing import List, Tuple
from dotenv import load_dotenv
from hybrid_search import SearchResult

# Load environment variables
load_dotenv()

class AdvancedReRanker:
    """Production re-ranker using cross-encoder models for precise ranking"""

    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'):
        """
        Initialize with a pre-trained cross-encoder model.
        ms-marco-MiniLM provides good balance of speed and accuracy.
        """
        self.model = CrossEncoder(model_name, max_length=512)

        # Cache for performance optimization
        self.cache = {}

    def rerank(self,
               query: str,
               results: List[SearchResult],
               top_k: int = 5,
               diversity_weight: float = 0.1) -> List[SearchResult]:
        """
        Re-rank search results using cross-encoder scoring.
        Includes diversity bonus to avoid redundant results.
        """

        if not results:
            return []

        # Prepare pairs for cross-encoder
        pairs = [[query, result.content] for result in results]

        # Get cross-encoder scores
        ce_scores = self.model.predict(pairs, batch_size=16)

        # Apply diversity penalty for similar content
        adjusted_scores = self._apply_diversity_penalty(
            results,
            ce_scores,
            diversity_weight
        )

        # Combine with original scores (weighted average)
        final_scores = []
        for i, result in enumerate(results):
            # 70% cross-encoder, 30% original score
            combined_score = (0.7 * adjusted_scores[i] +
                            0.3 * result.score)
            final_scores.append(combined_score)

        # Sort and return top k
        ranked_indices = np.argsort(final_scores)[::-1][:top_k]

        reranked_results = []
        for idx in ranked_indices:
            result = results[idx]
            result.score = float(final_scores[idx])
            reranked_results.append(result)

        return reranked_results

    def _apply_diversity_penalty(self,
                                 results: List[SearchResult],
                                 scores: np.ndarray,
                                 weight: float) -> np.ndarray:
        """
        Penalize redundant/similar results to improve diversity.
        Uses embedding similarity to detect near-duplicates.
        """

        adjusted_scores = scores.copy()
        selected = []

        for i in range(len(results)):
            if i == 0:
                selected.append(i)
                continue

            # Check similarity with already selected results
            max_similarity = 0
            for j in selected:
                # Simple text overlap as proxy for similarity
                overlap = self._text_overlap(
                    results[i].content,
                    results[j].content
                )
                max_similarity = max(max_similarity, overlap)

            # Apply penalty based on similarity
            penalty = weight * max_similarity
            adjusted_scores[i] = scores[i] * (1 - penalty)

            if adjusted_scores[i] > 0.3:  # Threshold for selection
                selected.append(i)

        return adjusted_scores

    def _text_overlap(self, text1: str, text2: str) -> float:
        """Calculate text overlap ratio using token intersection"""

        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())

        intersection = len(tokens1.intersection(tokens2))
        union = len(tokens1.union(tokens2))

        return intersection / union if union > 0 else 0