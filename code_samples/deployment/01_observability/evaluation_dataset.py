"""
Evaluation Dataset Builder
Creates evaluation datasets from production data for continuous improvement.
"""

from typing import List, Dict, Any
from dotenv import load_dotenv
from langsmith import Client
import os

# Load environment variables
load_dotenv()


class EvaluationDatasetBuilder:
    def __init__(self, client: Client = None):
        self.client = client or Client()
        self.dataset_name = "production-eval-set"

    def create_from_production(self, successful_runs: List[Dict[str, Any]]):
        """Convert successful production runs into eval dataset"""

        # Create or get dataset
        try:
            dataset = self.client.create_dataset(
                dataset_name=self.dataset_name,
                description="Auto-generated from production successes"
            )
        except Exception as e:
            print(f"Dataset may already exist or error occurred: {e}")
            # Try to get existing dataset
            datasets = list(self.client.list_datasets(dataset_name=self.dataset_name))
            if datasets:
                dataset = datasets[0]
            else:
                raise e

        # Add examples from production
        added_count = 0
        for run in successful_runs:
            try:
                # Only fast, successful runs
                if run.get("metrics", {}).get("latency_seconds", 0) < 5:
                    self.client.create_example(
                        inputs={"query": run.get("query", "")},
                        outputs={"result": run.get("result", "")},
                        dataset_id=dataset.id,
                        metadata={
                            "source": "production",
                            "latency": run.get("metrics", {}).get("latency_seconds", 0),
                            "cost": run.get("metrics", {}).get("total_cost_usd", 0)
                        }
                    )
                    added_count += 1
            except Exception as e:
                print(f"Failed to add example: {e}")
                continue

        print(f"Added {added_count} examples to evaluation dataset")
        return dataset

    def create_sample_dataset(self):
        """Create a sample evaluation dataset for testing"""
        sample_runs = [
            {
                "query": "What is the weather in New York?",
                "result": "The current weather in New York is 72°F with clear skies.",
                "metrics": {
                    "latency_seconds": 2.5,
                    "total_cost_usd": 0.02
                }
            },
            {
                "query": "Summarize the latest news in AI",
                "result": "Recent AI developments include advances in large language models...",
                "metrics": {
                    "latency_seconds": 4.2,
                    "total_cost_usd": 0.08
                }
            },
            {
                "query": "Calculate 15% tip on $45.67",
                "result": "A 15% tip on $45.67 would be $6.85, making the total $52.52.",
                "metrics": {
                    "latency_seconds": 1.8,
                    "total_cost_usd": 0.01
                }
            }
        ]

        return self.create_from_production(sample_runs)


if __name__ == "__main__":
    try:
        builder = EvaluationDatasetBuilder()

        # Create sample dataset for demonstration
        print("Creating sample evaluation dataset...")
        dataset = builder.create_sample_dataset()
        print(f"Sample dataset created successfully with ID: {dataset.id}")

    except Exception as e:
        print(f"Error creating evaluation dataset: {e}")
        print("Make sure your LANGCHAIN_API_KEY is set in the .env file")