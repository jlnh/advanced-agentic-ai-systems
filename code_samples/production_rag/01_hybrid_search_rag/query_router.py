"""
Query Router and Expansion - Production RAG Component
Routes queries to appropriate indexes and expands with synonyms.
"""

import os
from typing import List
from enum import Enum
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DocumentType(Enum):
    TECHNICAL = "technical"
    BUSINESS = "business"
    LEGAL = "legal"
    GENERAL = "general"

class QueryRouter:
    """Routes queries to appropriate specialized indexes"""

    def __init__(self):
        # Keywords indicating document types
        self.technical_indicators = [
            'error', 'code', 'function', 'api', 'debug',
            'implement', 'algorithm', 'performance', 'syntax'
        ]

        self.business_indicators = [
            'revenue', 'sales', 'strategy', 'market', 'customer',
            'growth', 'roi', 'metrics', 'dashboard'
        ]

        self.legal_indicators = [
            'policy', 'compliance', 'regulation', 'contract',
            'terms', 'agreement', 'liability', 'clause'
        ]

    def route_query(self, query: str) -> List[DocumentType]:
        """Determine which indexes to search"""

        query_lower = query.lower()
        scores = {}

        # Score for each document type
        scores[DocumentType.TECHNICAL] = sum(
            1 for term in self.technical_indicators
            if term in query_lower
        )

        scores[DocumentType.BUSINESS] = sum(
            1 for term in self.business_indicators
            if term in query_lower
        )

        scores[DocumentType.LEGAL] = sum(
            1 for term in self.legal_indicators
            if term in query_lower
        )

        # If no specific indicators, search general
        if max(scores.values()) == 0:
            return [DocumentType.GENERAL]

        # Return document types with score > 0
        selected = [
            doc_type for doc_type, score in scores.items()
            if score > 0
        ]

        return selected if selected else [DocumentType.GENERAL]


class QueryExpander:
    """Expands queries with synonyms and related terms"""

    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )

        # Domain-specific expansions
        self.technical_expansions = {
            'bug': ['error', 'issue', 'problem', 'defect'],
            'async': ['asynchronous', 'concurrent', 'parallel'],
            'api': ['endpoint', 'interface', 'service']
        }

    def expand_query(self, query: str) -> str:
        """Add synonyms and related terms to improve recall"""

        expanded_terms = [query]

        # Add domain-specific expansions
        for term, expansions in self.technical_expansions.items():
            if term in query.lower():
                expanded_terms.extend(expansions)

        # Use LLM for semantic expansion (optional)
        # expanded_terms.extend(self._llm_expand(query))

        return ' '.join(expanded_terms)