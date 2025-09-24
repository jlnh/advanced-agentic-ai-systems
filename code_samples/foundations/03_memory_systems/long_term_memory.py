"""
Long-term memory implementation using vector storage for semantic search.
"""

from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from datetime import datetime, timedelta
import json
import os


class LongTermMemory:
    """Persistent memory using vector storage for semantic search"""

    def __init__(self, embedding_model, storage_path="./memory_store"):
        self.embeddings = embedding_model
        self.storage_path = storage_path
        self.vectorstore = self._load_or_create_store()
        self.insights = self._load_insights()

    def _load_or_create_store(self):
        """Load existing vector store or create new one"""
        try:
            vectorstore = FAISS.load_local(
                self.storage_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            print("📚 Loaded existing memory store")
            return vectorstore
        except:
            # Create new store with initial document
            initial_doc = Document(
                page_content="Memory system initialized",
                metadata={"timestamp": datetime.now().isoformat(), "type": "system"}
            )
            vectorstore = FAISS.from_documents([initial_doc], self.embeddings)
            print("📚 Created new memory store")
            return vectorstore

    def _load_insights(self):
        """Load user insights and preferences"""
        try:
            with open(f"{self.storage_path}/insights.json", "r") as f:
                return json.load(f)
        except:
            return {
                "user_preferences": {},
                "successful_patterns": [],
                "domain_expertise": [],
                "interaction_stats": {}
            }

    def store_interaction(self, user_input, ai_response, context=None):
        """Store interaction with metadata for future retrieval"""
        interaction_text = f"User: {user_input}\nAI: {ai_response}"

        # Create document with rich metadata
        doc = Document(
            page_content=interaction_text,
            metadata={
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "ai_response": ai_response[:200],  # Truncate for metadata
                "type": "interaction",
                "context": context or {}
            }
        )

        # Add to vector store
        self.vectorstore.add_documents([doc])
        self._save_store()

    def extract_and_store_insights(self, conversation_summary):
        """Extract insights from conversation for future personalization"""
        # Simple pattern extraction (in production, use LLM for this)
        insights_to_extract = {
            "preferences": ["prefer", "like", "want", "need"],
            "expertise": ["experienced in", "familiar with", "work with"],
            "patterns": ["always", "usually", "typically", "often"]
        }

        summary_lower = conversation_summary.lower()

        for category, keywords in insights_to_extract.items():
            for keyword in keywords:
                if keyword in summary_lower:
                    # Extract context around keyword
                    start = max(0, summary_lower.find(keyword) - 50)
                    end = min(len(summary_lower), summary_lower.find(keyword) + 100)
                    context = conversation_summary[start:end]

                    if category not in self.insights:
                        self.insights[category] = []

                    self.insights[category].append({
                        "text": context.strip(),
                        "timestamp": datetime.now().isoformat(),
                        "confidence": 0.7  # Simple confidence score
                    })

        self._save_insights()

    def find_relevant_context(self, query, k=3):
        """Find relevant past interactions for current query"""
        try:
            docs = self.vectorstore.similarity_search(query, k=k)
            return [
                {
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "relevance": "high"  # In production, calculate actual relevance score
                }
                for doc in docs
            ]
        except:
            return []

    def get_user_profile(self):
        """Build user profile from stored insights"""
        profile = {
            "preferences": self.insights.get("preferences", [])[-3:],  # Recent preferences
            "expertise_areas": list(set([
                item["text"] for item in self.insights.get("expertise", [])
            ])),
            "interaction_count": len(self.insights.get("patterns", [])),
            "last_active": datetime.now().isoformat()
        }
        return profile

    def _save_store(self):
        """Save vector store to disk"""
        try:
            self.vectorstore.save_local(self.storage_path)
        except Exception as e:
            print(f"Failed to save memory store: {e}")

    def _save_insights(self):
        """Save insights to disk"""
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            with open(f"{self.storage_path}/insights.json", "w") as f:
                json.dump(self.insights, f, indent=2)
        except Exception as e:
            print(f"Failed to save insights: {e}")


class TokenOptimizedMemory:
    """Memory optimization strategies for token budget management"""

    def __init__(self, max_context_tokens=1500):
        self.max_tokens = max_context_tokens

    def optimize_context(self, context_parts):
        """Prioritize context by relevance and recency"""
        # Estimate tokens (rough: 1 token ≈ 4 characters)
        total_chars = sum(len(part) for part in context_parts)
        estimated_tokens = total_chars // 4

        if estimated_tokens <= self.max_tokens:
            return context_parts

        # Prioritize: recent > relevant > preferences
        optimized = []
        token_budget = self.max_tokens * 4  # Convert back to chars

        for part in context_parts:
            if len(part) <= token_budget:
                optimized.append(part)
                token_budget -= len(part)
            else:
                # Truncate long parts
                optimized.append(part[:token_budget] + "...")
                break

        return optimized


def compress_old_memories(vectorstore, days_old=30):
    """Compress memories older than threshold"""
    cutoff_date = datetime.now() - timedelta(days=days_old)

    # In production, implement actual compression
    # For now, we'll just mark old memories
    print(f"Compressing memories older than {cutoff_date}")

    # Strategy: Summarize old detailed interactions
    # Keep only key insights and patterns
    return "Compression completed"


def smart_memory_search(query, vectorstore, embeddings):
    """Enhanced memory search with filtering and ranking"""

    # Get initial candidates
    candidates = vectorstore.similarity_search(query, k=10)

    # Filter by recency and relevance
    filtered = []
    for doc in candidates:
        metadata = doc.metadata

        # Recency score (newer = higher)
        timestamp = datetime.fromisoformat(metadata.get("timestamp", "2020-01-01"))
        days_ago = (datetime.now() - timestamp).days
        recency_score = max(0, 1 - (days_ago / 365))  # Decay over year

        # Relevance score (placeholder - use actual similarity in production)
        relevance_score = 0.8  # Would calculate from embeddings

        # Combined score
        final_score = (relevance_score * 0.7) + (recency_score * 0.3)

        if final_score > 0.5:  # Threshold
            filtered.append((doc, final_score))

    # Return top-ranked memories
    filtered.sort(key=lambda x: x[1], reverse=True)
    return [doc for doc, score in filtered[:3]]