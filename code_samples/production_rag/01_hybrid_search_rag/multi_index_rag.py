"""
Multi-Index RAG - Production RAG System
Routes queries to appropriate specialized indexes based on content type.
"""

from typing import List, Dict, Optional
from dotenv import load_dotenv
from hybrid_search import HybridSearchEngine, SearchResult
from query_router import QueryRouter, DocumentType
from reranker import AdvancedReRanker

# Load environment variables
load_dotenv()

class MultiIndexRAG:
    """
    Production RAG system with multiple specialized indexes.
    Routes queries to appropriate indexes based on content type.
    """

    def __init__(self):
        # Specialized indexes with custom configurations
        self.indexes = {
            DocumentType.TECHNICAL: self._create_technical_index(),
            DocumentType.BUSINESS: self._create_business_index(),
            DocumentType.LEGAL: self._create_legal_index(),
            DocumentType.GENERAL: self._create_general_index()
        }

        # Query router
        self.router = QueryRouter()

        # Re-ranker
        self.reranker = AdvancedReRanker()

    def _create_technical_index(self) -> HybridSearchEngine:
        """Technical docs: high keyword weight for exact terms"""
        return HybridSearchEngine(
            semantic_weight=0.4,
            keyword_weight=0.6  # Higher weight for technical terms
        )

    def _create_business_index(self) -> HybridSearchEngine:
        """Business docs: balanced weights"""
        return HybridSearchEngine(
            semantic_weight=0.6,
            keyword_weight=0.4
        )

    def _create_legal_index(self) -> HybridSearchEngine:
        """Legal docs: emphasis on exact terminology"""
        return HybridSearchEngine(
            semantic_weight=0.3,
            keyword_weight=0.7  # Legal terms must match exactly
        )

    def _create_general_index(self) -> HybridSearchEngine:
        """General docs: semantic-heavy for concept matching"""
        return HybridSearchEngine(
            semantic_weight=0.8,
            keyword_weight=0.2
        )

    def index_document(self,
                       document: Dict,
                       doc_type: DocumentType):
        """Index document in appropriate specialized index"""

        # Apply type-specific preprocessing
        processed_doc = self._preprocess_document(document, doc_type)

        # Index in appropriate engine
        self.indexes[doc_type].index_documents([processed_doc])

    def _preprocess_document(self,
                            document: Dict,
                            doc_type: DocumentType) -> Dict:
        """Apply type-specific preprocessing"""

        if doc_type == DocumentType.TECHNICAL:
            # Preserve code blocks, extract function names
            document = self._process_technical_doc(document)
        elif doc_type == DocumentType.LEGAL:
            # Preserve section numbers, definitions
            document = self._process_legal_doc(document)
        elif doc_type == DocumentType.BUSINESS:
            # Extract metrics, dates, entities
            document = self._process_business_doc(document)

        return document

    def _process_technical_doc(self, document: Dict) -> Dict:
        """Process technical documents - preserve code structure"""
        # Implementation for technical document processing
        # This would include code-aware chunking, function extraction, etc.
        return document

    def _process_legal_doc(self, document: Dict) -> Dict:
        """Process legal documents - preserve sections and definitions"""
        # Implementation for legal document processing
        # This would include section-aware chunking, definition extraction, etc.
        return document

    def _process_business_doc(self, document: Dict) -> Dict:
        """Process business documents - extract metrics and entities"""
        # Implementation for business document processing
        # This would include metric extraction, date parsing, etc.
        return document

    def search(self,
              query: str,
              filter_dict: Dict = None,
              top_k: int = 5) -> List[SearchResult]:
        """
        Intelligent search across multiple indexes.
        Routes to appropriate index(es) based on query.
        """

        # Determine which indexes to search
        target_indexes = self.router.route_query(query)

        # Search relevant indexes
        all_results = []
        for doc_type in target_indexes:
            results = self.indexes[doc_type].search(
                query,
                k=20,  # Get more for re-ranking
                filter_dict=filter_dict
            )

            # Add index source to metadata
            for result in results:
                result.metadata['index_type'] = doc_type.value

            all_results.extend(results)

        # Re-rank combined results
        if all_results:
            reranked = self.reranker.rerank(
                query,
                all_results,
                top_k=top_k,
                diversity_weight=0.15
            )
            return reranked

        return []