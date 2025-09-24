"""
Main example script demonstrating the memory-enhanced agent system.
"""

from langchain_community.llms import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from short_term_memory import ShortTermMemory
from long_term_memory import LongTermMemory
from memory_enhanced_agent import MemoryEnhancedAgent
from test_memory_system import run_all_tests
from dotenv import load_dotenv
load_dotenv()

def initialize_memory_system():
    """Initialize the complete memory system with dependencies"""

    print("🔧 Initializing Memory System...")

    # Initialize LLM and embeddings (you'll need OpenAI API key)
    try:
        llm = OpenAI(temperature=0.7)
        embeddings = OpenAIEmbeddings()
        print("✅ LLM and embeddings initialized")
    except Exception as e:
        print(f"❌ Failed to initialize LLM/embeddings: {e}")
        print("Note: You need to set your OPENAI_API_KEY environment variable")
        return None, None, None, None

    # Create memory components
    short_memory = ShortTermMemory(llm, max_token_limit=800)
    print("💭 Short-term memory initialized")

    long_memory = LongTermMemory(embeddings)
    print("🧠 Long-term memory initialized")

    # For this example, we'll use a simple mock agent
    # In practice, you'd use your actual research agent
    class MockAgent:
        def invoke(self, inputs):
            user_input = inputs.get("input", "")
            return {
                "output": f"Mock response to: {user_input[:100]}..."
            }

    base_agent = MockAgent()

    # Create memory-enhanced agent
    memory_agent = MemoryEnhancedAgent(
        base_agent=base_agent,
        short_memory=short_memory,
        long_memory=long_memory
    )

    print("🧠 Memory-enhanced agent ready!")

    return memory_agent, short_memory, long_memory, base_agent


def interactive_demo():
    """Run an interactive demonstration of the memory system"""

    print("\n" + "="*60)
    print("🧠 MEMORY-ENHANCED AGENT DEMONSTRATION")
    print("="*60)

    # Initialize system
    memory_agent, short_memory, long_memory, base_agent = initialize_memory_system()

    if not memory_agent:
        return

    print("\nDemo Mode: Simulating user interactions...")

    # Simulate a series of interactions
    demo_interactions = [
        "I'm researching quantum computing algorithms for my PhD thesis.",
        "Can you help me find papers on quantum error correction?",
        "What are the latest developments in this field?",
        "Save the most relevant papers to my research folder."
    ]

    for i, user_input in enumerate(demo_interactions, 1):
        print(f"\n--- Interaction {i} ---")
        print(f"User: {user_input}")

        result = memory_agent.invoke(user_input)
        print(f"Agent: {result['output']}")

    # End session and show insights
    print("\n--- Session End ---")
    summary = memory_agent.end_session()
    print(f"Session Summary: {summary}")

    # Show user profile
    profile = long_memory.get_user_profile()
    print(f"\nUser Profile Learned:")
    print(f"- Preferences: {len(profile['preferences'])} items")
    print(f"- Expertise areas: {profile['expertise_areas']}")
    print(f"- Interactions: {profile['interaction_count']}")


def run_tests():
    """Run the test suite for the memory system"""

    print("\n" + "="*60)
    print("🧪 MEMORY SYSTEM TESTS")
    print("="*60)

    # Initialize system
    memory_agent, short_memory, long_memory, base_agent = initialize_memory_system()

    if not memory_agent:
        return

    # Run comprehensive tests
    run_all_tests(memory_agent, short_memory, long_memory)


if __name__ == "__main__":
    print("🚀 Memory-Enhanced Agent System")
    print("\nChoose an option:")
    print("1. Interactive Demo")
    print("2. Run Tests")
    print("3. Both")

    choice = input("\nEnter your choice (1/2/3): ").strip()

    if choice in ["1", "3"]:
        interactive_demo()

    if choice in ["2", "3"]:
        run_tests()

    if choice not in ["1", "2", "3"]:
        print("Invalid choice. Running demo by default...")
        interactive_demo()