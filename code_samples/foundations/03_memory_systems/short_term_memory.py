"""
Short-term memory implementation for conversation context management.
"""

from langchain.memory import ConversationSummaryBufferMemory
from datetime import datetime
import uuid


class ShortTermMemory:
    """Manages recent conversation context with automatic summarization"""

    def __init__(self, llm, max_token_limit=1000):
        self.memory = ConversationSummaryBufferMemory(
            llm=llm,
            max_token_limit=max_token_limit,
            return_messages=True,
            memory_key="chat_history"
        )
        self.session_id = str(uuid.uuid4())

    def add_interaction(self, user_input, ai_response):
        """Add a user-AI interaction to memory"""
        self.memory.save_context(
            {"input": user_input},
            {"output": ai_response}
        )

    def get_context(self):
        """Get current conversation context"""
        return self.memory.load_memory_variables({})

    def get_summary(self):
        """Get conversation summary for long-term storage"""
        variables = self.memory.load_memory_variables({})
        return variables.get("history", "No conversation history")

    def clear_session(self):
        """Start fresh session but preserve summary"""
        summary = self.get_summary()
        self.memory.clear()
        self.session_id = str(uuid.uuid4())
        return summary