# src/agentic_ai/core/memory/short_term.py
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from typing import Dict, Any
import uuid

class ShortTermMemory:
    """Manages recent conversation context with automatic summarization"""
    
    def __init__(self, llm=None, max_token_limit=1000):
        self.llm = llm or ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
        self.memory = ConversationSummaryBufferMemory(
            llm=self.llm,
            max_token_limit=max_token_limit,
            return_messages=True,
            memory_key="chat_history"
        )
        self.session_id = str(uuid.uuid4())
        
    def add_interaction(self, user_input: str, ai_response: str):
        """Add a user-AI interaction to memory"""
        self.memory.save_context(
            {"input": user_input},
            {"output": ai_response}
        )
        
    def get_context(self) -> Dict[str, Any]:
        """Get current conversation context"""
        return self.memory.load_memory_variables({})
    
    def get_summary(self) -> str:
        """Get conversation summary for long-term storage"""
        variables = self.memory.load_memory_variables({})
        return variables.get("history", "No conversation history")
    
    def clear_session(self) -> str:
        """Start fresh session but preserve summary"""
        summary = self.get_summary()
        self.memory.clear()
        self.session_id = str(uuid.uuid4())
        return summary