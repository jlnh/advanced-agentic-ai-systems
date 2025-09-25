from typing import List, NamedTuple, Dict
from dotenv import load_dotenv
import os
import re

# Load environment variables
load_dotenv()


class Tool(NamedTuple):
    """Simple tool representation"""
    name: str
    description: str


class SimpleToolOptimizer:
    """Simple tool optimizer that doesn't require embeddings for testing"""

    def __init__(self, all_tools: List[Tool]):
        self.all_tools = all_tools

    def select_tools_simple(self, query: str, max_tools: int = 5) -> List[Tool]:
        """Select tools based on keyword matching"""
        query_lower = query.lower()
        tool_scores = []

        for tool in self.all_tools:
            score = 0
            tool_keywords = tool.name.lower().split('_') + tool.description.lower().split()

            # Check for keyword matches
            for word in query_lower.split():
                for keyword in tool_keywords:
                    if word in keyword or keyword in word:
                        score += 1

            # Boost essential tools
            if tool.name in ["web_search", "calculator"]:
                score += 2

            tool_scores.append((tool, score))

        # Sort by relevance and take top N
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        selected_tools = [tool for tool, score in tool_scores[:max_tools] if score > 0]

        return selected_tools

    def get_optimization_stats(self, query: str, max_tools: int = 5) -> Dict:
        """Get detailed optimization statistics"""
        selected_tools = self.select_tools_simple(query, max_tools)

        # Calculate token savings
        all_tools_tokens = sum(len(t.description.split()) * 1.3 for t in self.all_tools)
        selected_tokens = sum(len(t.description.split()) * 1.3 for t in selected_tools)
        savings_percent = (1 - selected_tokens / all_tools_tokens) * 100 if all_tools_tokens > 0 else 0

        return {
            "query": query,
            "total_tools_available": len(self.all_tools),
            "tools_selected": len(selected_tools),
            "selected_tools": [{"name": t.name, "description": t.description} for t in selected_tools],
            "token_reduction_percent": savings_percent,
            "estimated_tokens_saved": all_tools_tokens - selected_tokens
        }


def create_sample_tools() -> List[Tool]:
    """Create a sample set of tools for testing"""
    return [
        Tool("web_search", "Search the internet for current information and news"),
        Tool("calculator", "Perform mathematical calculations and computations"),
        Tool("weather_api", "Get current weather conditions and forecasts"),
        Tool("email_sender", "Send emails to specified recipients"),
        Tool("calendar", "Manage calendar events and scheduling"),
        Tool("file_manager", "Read, write, and manage files on the system"),
        Tool("database_query", "Query databases and retrieve data"),
        Tool("image_generator", "Generate images using AI models"),
        Tool("text_translator", "Translate text between different languages"),
        Tool("stock_api", "Get stock prices and market data"),
        Tool("news_api", "Fetch latest news from various sources"),
        Tool("social_media", "Post and manage social media content"),
        Tool("pdf_processor", "Process and extract text from PDF documents"),
        Tool("csv_processor", "Read and manipulate CSV files"),
        Tool("json_processor", "Parse and manipulate JSON data"),
        Tool("xml_processor", "Parse and process XML documents"),
        Tool("web_scraper", "Extract data from websites"),
        Tool("audio_processor", "Process and analyze audio files"),
        Tool("video_processor", "Process and analyze video files"),
        Tool("encryption", "Encrypt and decrypt sensitive data")
    ]


if __name__ == "__main__":
    # Create sample tools
    tools = create_sample_tools()
    optimizer = SimpleToolOptimizer(tools)

    # Test queries
    test_queries = [
        "What's the current weather in New York?",
        "Calculate the compound interest on $1000",
        "Send an email to my team about the meeting",
        "Find the latest news about artificial intelligence",
        "Translate this text to French",
        "Generate an image of a sunset",
        "What's the stock price of Apple?",
    ]

    print("Simple Tool Optimization Test")
    print("=" * 50)

    # Analyze each query
    for query in test_queries:
        stats = optimizer.get_optimization_stats(query)
        print(f"\nQuery: {query}")
        print(f"Tools selected: {stats['tools_selected']}/{stats['total_tools_available']}")
        print(f"Token reduction: {stats['token_reduction_percent']:.1f}%")
        print("Selected tools:", ", ".join([t["name"] for t in stats["selected_tools"]]))