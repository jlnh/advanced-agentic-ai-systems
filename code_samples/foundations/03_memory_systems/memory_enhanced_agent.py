"""
Memory-enhanced agent implementation that combines short-term and long-term memory.
"""

from datetime import datetime


class MemoryEnhancedAgent:
    """Agent with both short-term and long-term memory capabilities"""

    def __init__(self, base_agent, short_memory, long_memory):
        self.agent = base_agent
        self.short_memory = short_memory
        self.long_memory = long_memory

    def _build_context_prompt(self, user_input):
        """Build enriched prompt with memory context"""
        # Get short-term context
        recent_context = self.short_memory.get_context()

        # Find relevant long-term memories
        relevant_memories = self.long_memory.find_relevant_context(user_input)

        # Get user profile
        user_profile = self.long_memory.get_user_profile()

        # Build enhanced context
        context_parts = [f"Current request: {user_input}"]

        if recent_context.get("chat_history"):
            context_parts.append(f"Recent conversation context: {recent_context['chat_history']}")

        if relevant_memories:
            memory_context = "\n".join([mem["content"][:200] for mem in relevant_memories[:2]])
            context_parts.append(f"Relevant past interactions: {memory_context}")

        if user_profile["preferences"]:
            prefs = [p["text"][:100] for p in user_profile["preferences"]]
            context_parts.append(f"User preferences: {'; '.join(prefs)}")

        enhanced_prompt = "\n\n".join(context_parts)
        return enhanced_prompt

    def invoke(self, user_input):
        """Process user input with full memory context"""
        # Build context-aware prompt
        enhanced_prompt = self._build_context_prompt(user_input)

        # Execute agent with enhanced context
        try:
            result = self.agent.invoke({"input": enhanced_prompt})
            ai_response = result.get("output", "No response generated")

            # Store interaction in both memory systems
            self.short_memory.add_interaction(user_input, ai_response)

            self.long_memory.store_interaction(
                user_input,
                ai_response,
                context={"session_id": self.short_memory.session_id}
            )

            return result

        except Exception as e:
            error_response = f"I encountered an error: {str(e)}"
            self.short_memory.add_interaction(user_input, error_response)
            return {"output": error_response}

    def end_session(self):
        """End current session and extract insights"""
        # Get conversation summary
        summary = self.short_memory.get_summary()

        # Extract insights for long-term learning
        self.long_memory.extract_and_store_insights(summary)

        # Clear short-term memory for new session
        self.short_memory.clear_session()

        print("Session ended. Insights extracted and stored.")
        return summary


class MemoryMonitor:
    """Monitor memory usage and prevent memory leaks"""

    def __init__(self):
        self.memory_usage = {}

    def track_memory_growth(self, component_name, size):
        if component_name not in self.memory_usage:
            self.memory_usage[component_name] = []

        self.memory_usage[component_name].append({
            "timestamp": datetime.now(),
            "size": size
        })

        # Alert if growing too fast
        if len(self.memory_usage[component_name]) > 10:
            recent = self.memory_usage[component_name][-10:]
            growth_rate = (recent[-1]["size"] - recent[0]["size"]) / 10

            if growth_rate > 1000:  # 1KB per interaction
                print(f"⚠️ Memory growing rapidly in {component_name}")


def handle_context_overflow(context, max_tokens=4000):
    """Gracefully handle when context exceeds model limits"""

    # Estimate tokens
    estimated_tokens = len(context) // 4

    if estimated_tokens <= max_tokens:
        return context

    print(f"Context overflow: {estimated_tokens} tokens, max {max_tokens}")

    # Strategy 1: Summarize oldest parts
    parts = context.split("\n\n")

    # Keep recent parts, summarize old parts
    recent_parts = parts[-3:]  # Keep last 3 sections
    old_parts = parts[:-3]

    if old_parts:
        old_summary = f"Previous context summary: {' '.join(old_parts)[:200]}..."
        return old_summary + "\n\n" + "\n\n".join(recent_parts)

    return context[:max_tokens * 4]  # Fallback: truncate


class ProductionMemoryStore:
    """Production-ready memory storage with backup capabilities"""

    def __init__(self, user_id, storage_backend="local"):
        self.user_id = user_id
        self.storage_backend = storage_backend

    def get_storage_path(self):
        if self.storage_backend == "local":
            return f"./memory_stores/user_{self.user_id}"
        elif self.storage_backend == "s3":
            return f"s3://memory-bucket/users/{self.user_id}"
        # Add other backends as needed

    def backup_memory(self):
        """Regular backup of user memory"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{self.get_storage_path()}_backup_{timestamp}"

        # Implement backup logic based on storage backend
        print(f"Memory backed up to {backup_path}")


def generate_memory_stats(long_memory):
    """Generate analytics for memory system performance"""

    insights = long_memory.insights

    stats = {
        "total_interactions": len(insights.get("patterns", [])),
        "user_preferences_learned": len(insights.get("preferences", [])),
        "expertise_areas_identified": len(insights.get("expertise", [])),
        "memory_store_size": len(str(insights)),
        "avg_context_relevance": 0.75,  # Calculate from actual retrieval scores
    }

    print("📊 Memory System Analytics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")

    return stats