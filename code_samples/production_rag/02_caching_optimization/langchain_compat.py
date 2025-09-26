"""
LangChain compatibility layer to handle different versions and missing dependencies
"""

# Handle ChatOpenAI import
try:
    from langchain_openai import ChatOpenAI
except ImportError:
    class MockChatOpenAI:
        def __init__(self, model="mock-model", temperature=0.7, max_tokens=1000, **kwargs):
            self.model = model
            self.temperature = temperature
            self.max_tokens = max_tokens

        def invoke(self, messages):
            if isinstance(messages, str):
                return f"Mock response for: {messages[:50]}..."
            return "Mock response"

    ChatOpenAI = MockChatOpenAI

# Handle OpenAI embeddings import
try:
    from langchain_openai import OpenAIEmbeddings
except ImportError:
    try:
        from langchain.embeddings import OpenAIEmbeddings
    except ImportError:
        class MockOpenAIEmbeddings:
            def __init__(self, model="mock-embedding-model", **kwargs):
                self.model = model

            def embed_query(self, query):
                # Simple hash-based mock embedding
                import hashlib
                hash_obj = hashlib.md5(query.encode())
                # Convert hash to list of floats between -1 and 1
                hash_bytes = hash_obj.digest()
                embedding = [(b - 128) / 128.0 for b in hash_bytes[:10]]  # 10-dim mock embedding
                return embedding

        OpenAIEmbeddings = MockOpenAIEmbeddings

# Handle callback manager import
try:
    from langchain_community.callbacks.manager import get_openai_callback
except ImportError:
    try:
        from langchain.callbacks import get_openai_callback
    except ImportError:
        class MockCallback:
            def __init__(self):
                self.total_cost = 0.05  # Mock cost
                self.total_tokens = 100  # Mock tokens

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

        def get_openai_callback():
            return MockCallback()

# Handle agents import
try:
    from langchain.agents import create_react_agent, AgentExecutor
except ImportError:
    class MockAgentExecutor:
        def __init__(self, agent=None, tools=None, **kwargs):
            self.agent = agent
            self.tools = tools

        async def ainvoke(self, input_dict):
            query = input_dict.get('input', 'unknown query')
            return {
                "output": f"Mock agent response for: {query[:50]}...",
                "intermediate_steps": []
            }

        def invoke(self, input_dict):
            query = input_dict.get('input', 'unknown query')
            return {
                "output": f"Mock agent response for: {query[:50]}...",
                "intermediate_steps": []
            }

    def create_react_agent(llm, tools, prompt):
        return "mock_agent"

    AgentExecutor = MockAgentExecutor

# Handle prompts import
try:
    from langchain.prompts import PromptTemplate
except ImportError:
    class MockPromptTemplate:
        def __init__(self, input_variables=None, template="", **kwargs):
            self.input_variables = input_variables or []
            self.template = template

    PromptTemplate = MockPromptTemplate

# Export all the imports
__all__ = [
    'ChatOpenAI',
    'OpenAIEmbeddings',
    'get_openai_callback',
    'create_react_agent',
    'AgentExecutor',
    'PromptTemplate'
]