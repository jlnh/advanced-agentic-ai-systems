#!/usr/bin/env python3
"""
Simple test script to demonstrate API functionality.
Run this after starting the API with docker-compose or uvicorn.
"""

import requests
import json
import time
from dotenv import load_dotenv
import os

load_dotenv()

# API configuration
API_BASE_URL = "http://localhost:8000"
API_KEY = os.getenv("API_KEYS", "demo-key-123").split(",")[0]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}


def test_health_check():
    """Test the health endpoint"""
    print("🔍 Testing health check...")
    response = requests.get(f"{API_BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def test_sync_execution():
    """Test synchronous agent execution"""
    print("🤖 Testing synchronous agent execution...")

    payload = {
        "task": "Summarize the benefits of using FastAPI for building APIs",
        "agent_type": "general",
        "context": {"format": "bullet_points"},
        "async_execution": False
    }

    response = requests.post(
        f"{API_BASE_URL}/agent/execute",
        headers=headers,
        json=payload
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_async_execution():
    """Test asynchronous agent execution"""
    print("⏳ Testing asynchronous agent execution...")

    payload = {
        "task": "Explain the concept of microservices architecture",
        "agent_type": "research",
        "context": {"depth": "detailed"},
        "async_execution": True
    }

    # Submit async task
    response = requests.post(
        f"{API_BASE_URL}/agent/execute",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        task_data = response.json()
        task_id = task_data["task_id"]
        print(f"Task submitted: {task_id}")

        # Check task status
        time.sleep(2)  # Wait for processing
        status_response = requests.get(
            f"{API_BASE_URL}/agent/status/{task_id}",
            headers=headers
        )

        print(f"Task status: {status_response.status_code}")
        print(f"Response: {json.dumps(status_response.json(), indent=2)}")
    else:
        print(f"Failed to submit task: {response.status_code}")
        print(f"Error: {response.text}")
    print()


def test_rate_limiting():
    """Test rate limiting by making multiple rapid requests"""
    print("🚦 Testing rate limiting...")

    payload = {
        "task": "Quick test task",
        "agent_type": "general"
    }

    for i in range(12):  # Exceed the default limit of 10
        response = requests.post(
            f"{API_BASE_URL}/agent/execute",
            headers=headers,
            json=payload
        )

        if response.status_code == 429:
            print(f"Request {i+1}: Rate limited (429)")
            print(f"Rate limit response: {response.json()}")
            break
        else:
            print(f"Request {i+1}: Success ({response.status_code})")
    print()


def test_metrics():
    """Test the metrics endpoint"""
    print("📊 Testing metrics endpoint...")
    response = requests.get(f"{API_BASE_URL}/metrics")
    print(f"Status: {response.status_code}")
    print("Metrics available (first 5 lines):")
    print("\n".join(response.text.split("\n")[:5]))
    print()


def test_invalid_api_key():
    """Test authentication with invalid API key"""
    print("🔐 Testing invalid API key...")

    invalid_headers = {
        "Authorization": "Bearer invalid-key",
        "Content-Type": "application/json"
    }

    payload = {"task": "Test task"}

    response = requests.post(
        f"{API_BASE_URL}/agent/execute",
        headers=invalid_headers,
        json=payload
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()


def main():
    """Run all tests"""
    print("🧪 Starting API tests...\n")

    try:
        test_health_check()
        test_sync_execution()
        test_async_execution()
        test_metrics()
        test_invalid_api_key()
        test_rate_limiting()  # Run this last as it may block further requests

        print("✅ All tests completed!")

    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")


if __name__ == "__main__":
    main()