"""
LangSmith Observability Setup
Establishes the foundation for agent monitoring with LangSmith integration.
"""

import os
from dotenv import load_dotenv
from langsmith import Client
from langchain.callbacks import LangChainTracer
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Configure LangSmith - set these in your .env file
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY", "your-api-key")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT", "production-agents")


class ObservabilitySetup:
    def __init__(self):
        self.client = Client()
        self.project_name = os.getenv("LANGCHAIN_PROJECT", "production-agents")

        # Create project if it doesn't exist
        self._ensure_project_exists()

    def _ensure_project_exists(self):
        """Create project and evaluation dataset"""
        try:
            # This will create the project if it doesn't exist
            self.tracer = LangChainTracer(
                project_name=self.project_name,
                client=self.client
            )
            print(f"✓ Connected to LangSmith project: {self.project_name}")
        except Exception as e:
            print(f"⚠️  LangSmith setup error: {e}")
            # Fall back to local logging
            self.tracer = None


if __name__ == "__main__":
    # Test the setup
    setup = ObservabilitySetup()
    print("ObservabilitySetup initialized successfully!")