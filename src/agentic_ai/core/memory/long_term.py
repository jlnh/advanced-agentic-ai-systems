# src/agentic_ai/core/memory/long_term.py
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.schema import Document
from typing import List, Dict, Any, Optional
import json
import os
from datetime import datetime
import hashlib

class LongTermMemory:
    """Persistent memory using vector storage for semantic search"""
    
    def __init__(self, storage_path="./memory_store"):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.storage_path = storage_path
        self.vectorstore = self._load_or_create_store()
        self.insights = self._load_insights()
        
    def _load_or_create_store(self):
        """Load existing vector store or create new one"""
        try:
            if os.path.exists(self.storage_path):
                vectorstore = FAISS.load_local(
                    self.storage_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print(f"📚 Loaded existing memory store from {self.storage_path}")
                return vectorstore
        except Exception as e:
            print(f"⚠️ Failed to load existing store: {e}")
        
        # Create new store with initial document
        initial_doc = Document(
            page_content="Memory system initialized",
            metadata={"timestamp": datetime.now().isoformat(), "type": "system"}
        )
        vectorstore = FAISS.from_documents([initial_doc], self.embeddings)
        print("📚 Created new memory store")
        return vectorstore
    
    def _load_insights(self) -> Dict[str, Any]:
        """Load user insights and preferences"""
        insights_file = os.path.join(self.storage_path, "insights.json")
        try:
            with open(insights_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "user_preferences": {},
                "successful_patterns": [],
                "domain_expertise": [],
                "interaction_stats": {}
            }
    
    def store_interaction(self, user_input: str, ai_response: str, context: Dict[str, Any] = None):
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
        
    def find_relevant_context(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
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
        except Exception as e:
            print(f"⚠️ Error finding relevant context: {e}")
            return []
    
    def get_user_profile(self) -> Dict[str, Any]:
        """Build user profile from stored insights"""
        profile = {
            "preferences": self.insights.get("user_preferences", {}),
            "expertise_areas": self.insights.get("domain_expertise", []),
            "interaction_count": len(self.insights.get("successful_patterns", [])),
            "last_active": datetime.now().isoformat()
        }
        return profile
    
    def _save_store(self):
        """Save vector store to disk"""
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            self.vectorstore.save_local(self.storage_path)
        except Exception as e:
            print(f"⚠️ Failed to save memory store: {e}")
    
    def _save_insights(self):
        """Save insights to disk"""
        try:
            os.makedirs(self.storage_path, exist_ok=True)
            insights_file = os.path.join(self.storage_path, "insights.json")
            with open(insights_file, "w") as f:
                json.dump(self.insights, f, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save insights: {e}")