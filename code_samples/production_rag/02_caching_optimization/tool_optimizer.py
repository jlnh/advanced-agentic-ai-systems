from typing import List, NamedTuple, Dict
from sklearn.metrics.pairwise import cosine_similarity
from langchain_compat import OpenAIEmbeddings
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


class Tool(NamedTuple):
    """Simple tool representation"""
    name: str
    description: str


class ToolOptimizer:
    """Dynamically select minimum required tools based on query"""

    def __init__(self, all_tools: List[Tool]):
        self.all_tools = all_tools
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        # Pre-compute tool embeddings for fast matching
        self.tool_embeddings = {}
        for tool in all_tools:
            desc_embedding = self.embeddings.embed_query(
                f"{tool.name}: {tool.description}"
            )
            self.tool_embeddings[tool.name] = desc_embedding

    def select_tools(self, query: str, max_tools: int = 5) -> List[Tool]:
        """Select only relevant tools for the query"""

        # Embed the query
        query_embedding = self.embeddings.embed_query(query)

        # Score each tool's relevance
        tool_scores = []
        for tool in self.all_tools:
            similarity = cosine_similarity(
                [query_embedding],
                [self.tool_embeddings[tool.name]]
            )[0][0]

            # Boost essential tools
            if tool.name in ["web_search", "calculator"]:
                similarity += 0.1

            tool_scores.append((tool, similarity))

        # Sort by relevance and take top N
        tool_scores.sort(key=lambda x: x[1], reverse=True)
        selected_tools = [tool for tool, score in tool_scores[:max_tools]]

        return selected_tools

    def get_optimization_stats(self, query: str, max_tools: int = 5) -> Dict:
        """Get detailed optimization statistics"""
        selected_tools = self.select_tools(query, max_tools)

        # Calculate token savings
        all_tools_tokens = sum(len(t.description.split()) * 1.3 for t in self.all_tools)
        selected_tokens = sum(len(t.description.split()) * 1.3 for t in selected_tools)
        savings_percent = (1 - selected_tokens / all_tools_tokens) * 100

        return {
            "query": query,
            "total_tools_available": len(self.all_tools),
            "tools_selected": len(selected_tools),
            "selected_tools": [{"name": t.name, "description": t.description} for t in selected_tools],
            "token_reduction_percent": savings_percent,
            "estimated_tokens_saved": all_tools_tokens - selected_tokens
        }

    def analyze_tool_usage_pattern(self, queries: List[str], max_tools: int = 5) -> Dict:
        """Analyze tool usage patterns across multiple queries"""
        tool_usage_count = {}
        total_selections = 0

        for query in queries:
            selected_tools = self.select_tools(query, max_tools)
            total_selections += len(selected_tools)

            for tool in selected_tools:
                tool_usage_count[tool.name] = tool_usage_count.get(tool.name, 0) + 1

        # Sort tools by usage frequency
        sorted_usage = sorted(tool_usage_count.items(), key=lambda x: x[1], reverse=True)

        return {
            "total_queries": len(queries),
            "average_tools_per_query": total_selections / len(queries),
            "tool_usage_frequency": [
                {
                    "tool_name": name,
                    "usage_count": count,
                    "usage_percentage": (count / len(queries)) * 100
                }
                for name, count in sorted_usage
            ],
            "most_popular_tools": sorted_usage[:5]
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
    optimizer = ToolOptimizer(tools)

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

    print("Tool Optimization Analysis")
    print("=" * 50)

    # Analyze each query
    for query in test_queries:
        stats = optimizer.get_optimization_stats(query)
        print(f"\nQuery: {query}")
        print(f"Tools selected: {stats['tools_selected']}/{stats['total_tools_available']}")
        print(f"Token reduction: {stats['token_reduction_percent']:.1f}%")
        print("Selected tools:", ", ".join([t["name"] for t in stats["selected_tools"]]))

    # Overall usage pattern analysis
    print(f"\n\nTool Usage Pattern Analysis")
    print("=" * 40)
    usage_stats = optimizer.analyze_tool_usage_pattern(test_queries)
    print(f"Average tools per query: {usage_stats['average_tools_per_query']:.1f}")
    print(f"\nMost popular tools:")
    for tool_data in usage_stats["tool_usage_frequency"][:5]:
        print(f"- {tool_data['tool_name']}: {tool_data['usage_count']} times ({tool_data['usage_percentage']:.1f}%)")