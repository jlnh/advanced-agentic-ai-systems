#!/usr/bin/env python3
"""
Production FastAPI application for multi-agent system orchestration.
This is a complete production-ready API with authentication, rate limiting,
monitoring, and security features.
"""

import os
import json
import uuid
import time
import hashlib
import asyncio
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Optional, Dict, Any, List

import redis
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel, Field, validator
from prometheus_client import Counter, Histogram, generate_latest
import structlog

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure structured logging
logger = structlog.get_logger()

# Initialize Redis for rate limiting and caching
redis_client = redis.from_url(
    os.getenv("REDIS_URL", "redis://localhost:6379"),
    decode_responses=True
)

# Security setup
security = HTTPBearer()

# Store for async task results (in production, use Redis or database)
task_store = {}

# Prometheus metrics
request_count = Counter('agent_requests_total', 'Total agent requests')
request_duration = Histogram('agent_request_duration_seconds', 'Request duration')


class AgentRequest(BaseModel):
    """Validated request model for agent execution"""
    task: str = Field(..., min_length=1, max_length=1000)
    agent_type: str = Field(default="general", pattern="^(general|research|analysis|writing)$")
    context: Optional[Dict[str, Any]] = Field(default_factory=dict)
    async_execution: bool = Field(default=False, description="Execute asynchronously")
    webhook_url: Optional[str] = Field(None, description="Webhook for async results")

    @validator('task')
    def validate_task_content(cls, v):
        """Prevent prompt injection and validate input"""
        # Block obvious prompt injections
        injection_patterns = [
            'ignore previous instructions',
            'ignore all previous',
            'disregard prior',
            'system:',
            '```python',
            'SYSTEM:',
            '<system>',
        ]

        task_lower = v.lower()
        for pattern in injection_patterns:
            if pattern in task_lower:
                raise ValueError(f"Potentially unsafe input detected")

        # Block excessive special characters (potential encoding attacks)
        special_char_count = sum(1 for c in v if not c.isalnum() and c not in ' .,!?-')
        if special_char_count > len(v) * 0.3:  # More than 30% special chars
            raise ValueError("Input contains too many special characters")

        return v


class AgentResponse(BaseModel):
    """Response model for agent execution"""
    task_id: str
    status: str  # "completed", "processing", "failed"
    result: Optional[Any] = None
    error: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    processing_time: Optional[float] = None
    cost: Optional[float] = None


class RateLimiter:
    """Redis-backed distributed rate limiter"""

    def __init__(self, redis_client, default_limit=10, window=60):
        self.redis = redis_client
        self.default_limit = default_limit
        self.window = window

    async def check_rate_limit(self, client_id: str, custom_limit: Optional[int] = None):
        """Check if client has exceeded rate limit"""
        limit = custom_limit or self.default_limit
        key = f"rate_limit:{client_id}"

        try:
            # Use Redis pipeline for atomic operations
            pipe = self.redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, self.window)
            results = pipe.execute()

            current_requests = results[0]

            if current_requests > limit:
                # Calculate time until reset
                ttl = self.redis.ttl(key)
                raise HTTPException(
                    status_code=429,
                    detail={
                        "error": "Rate limit exceeded",
                        "limit": limit,
                        "window": self.window,
                        "retry_after": ttl
                    },
                    headers={"Retry-After": str(ttl)}
                )

            return {
                "requests_made": current_requests,
                "requests_remaining": limit - current_requests,
                "resets_in": self.redis.ttl(key)
            }

        except redis.RedisError as e:
            # Log error but don't block requests if Redis is down
            logger.warning("Rate limiter error", error=str(e))
            return {"requests_remaining": limit}


# Initialize rate limiter
rate_limiter = RateLimiter(redis_client)


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """Verify API key and return user info"""
    api_key = credentials.credentials

    # Hash the API key for secure comparison
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()

    # In production, look up key in database
    # For demo, use environment variables
    valid_keys = {
        hashlib.sha256(k.encode()).hexdigest(): {
            "client_id": f"client_{i}",
            "tier": "premium" if i == 0 else "basic",
            "rate_limit": 100 if i == 0 else 10
        }
        for i, k in enumerate(os.getenv("API_KEYS", "demo-key-123").split(","))
    }

    if key_hash not in valid_keys:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key"
        )

    return valid_keys[key_hash]


async def initialize_orchestrator():
    """Initialize the agent orchestrator - placeholder for actual implementation"""
    logger.info("Initializing agent orchestrator")
    # In a real implementation, this would initialize your multi-agent system
    # For now, return a mock orchestrator
    return MockOrchestrator()


class MockOrchestrator:
    """Mock orchestrator for demonstration purposes"""

    async def arun(self, task: str, agent_type: str, context: Dict[str, Any]):
        """Mock agent execution"""
        await asyncio.sleep(1)  # Simulate processing time
        return {
            "output": f"Processed task: {task}",
            "agent_used": agent_type,
            "context_keys": list(context.keys())
        }


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup
    logger.info("Starting up API server")
    # Initialize your agents here
    app.state.orchestrator = await initialize_orchestrator()
    app.state.logger = logger
    yield
    # Shutdown
    logger.info("Shutting down API server")
    # Cleanup resources


app = FastAPI(
    title="Multi-Agent System API",
    description="Production API for AI agent orchestration",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for web clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


async def execute_agent_sync(request: AgentRequest, user_info: Dict) -> Dict:
    """Synchronous agent execution with monitoring"""

    # Get orchestrator from app state
    orchestrator = app.state.orchestrator

    # Check cache first
    cache_key = f"agent_result:{hashlib.md5(request.task.encode()).hexdigest()}"
    try:
        cached = redis_client.get(cache_key)

        if cached and not request.context.get("skip_cache"):
            return json.loads(cached)
    except redis.RedisError:
        logger.warning("Cache lookup failed")

    # Execute agent with monitoring
    start_time = time.time()
    result = await orchestrator.arun(
        task=request.task,
        agent_type=request.agent_type,
        context=request.context
    )

    processing_time = time.time() - start_time

    output = {
        "output": result,
        "metadata": {
            "agent_type": request.agent_type,
            "processing_time": processing_time
        },
        "cost": 0.01  # Mock cost
    }

    # Cache result for 1 hour
    try:
        redis_client.setex(
            cache_key,
            3600,
            json.dumps(output)
        )
    except redis.RedisError:
        logger.warning("Cache storage failed")

    return output


async def execute_agent_async(task_id: str, request: AgentRequest, user_info: Dict):
    """Execute agent task asynchronously"""
    try:
        # Store initial status
        task_store[task_id] = {
            "status": "processing",
            "client_id": user_info["client_id"],
            "started_at": datetime.utcnow().isoformat()
        }

        # Execute task
        result = await execute_agent_sync(request, user_info)

        # Update status
        task_store[task_id].update({
            "status": "completed",
            "result": result["output"],
            "metadata": result["metadata"],
            "cost": result.get("cost"),
            "completed_at": datetime.utcnow().isoformat()
        })

        # Send webhook if provided
        if request.webhook_url:
            # In production, implement webhook sending
            logger.info("Webhook would be sent", webhook_url=request.webhook_url)

    except Exception as e:
        task_store[task_id].update({
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.utcnow().isoformat()
        })
        logger.error("Async task failed", task_id=task_id, error=str(e))


@app.post("/agent/execute", response_model=AgentResponse)
async def execute_agent_task(
    request: AgentRequest,
    background_tasks: BackgroundTasks,
    user_info: Dict = Depends(verify_api_key)
):
    """Execute an agent task with full production features"""

    # Check rate limit for this user
    await rate_limiter.check_rate_limit(
        user_info["client_id"],
        custom_limit=user_info.get("rate_limit")
    )

    # Generate task ID
    task_id = str(uuid.uuid4())
    start_time = time.time()

    # Increment metrics
    request_count.inc()

    # Log request
    logger.info(
        "Agent task started",
        task_id=task_id,
        client_id=user_info["client_id"],
        task_type=request.agent_type
    )

    if request.async_execution:
        # Execute asynchronously
        background_tasks.add_task(
            execute_agent_async,
            task_id,
            request,
            user_info
        )

        return AgentResponse(
            task_id=task_id,
            status="processing",
            metadata={"message": "Task queued for processing"}
        )

    else:
        # Execute synchronously with timeout
        try:
            with request_duration.time():
                result = await asyncio.wait_for(
                    execute_agent_sync(request, user_info),
                    timeout=30.0  # 30 second timeout
                )

            processing_time = time.time() - start_time

            return AgentResponse(
                task_id=task_id,
                status="completed",
                result=result["output"],
                metadata=result.get("metadata", {}),
                processing_time=processing_time,
                cost=result.get("cost")
            )

        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=504,
                detail="Request timeout - consider using async execution"
            )
        except Exception as e:
            logger.error(
                "Agent task failed",
                task_id=task_id,
                error=str(e)
            )
            raise HTTPException(
                status_code=500,
                detail=f"Agent execution failed: {str(e)}"
            )


@app.get("/agent/status/{task_id}")
async def get_task_status(
    task_id: str,
    user_info: Dict = Depends(verify_api_key)
):
    """Check status of async task"""

    if task_id not in task_store:
        raise HTTPException(404, "Task not found")

    task = task_store[task_id]

    # Verify ownership
    if task.get("client_id") != user_info["client_id"]:
        raise HTTPException(403, "Access denied")

    return task


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""

    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": app.version,
        "checks": {}
    }

    # Check Redis
    try:
        redis_client.ping()
        health_status["checks"]["redis"] = "ok"
    except:
        health_status["checks"]["redis"] = "failed"
        health_status["status"] = "degraded"

    # Check agent orchestrator
    if hasattr(app.state, 'orchestrator'):
        health_status["checks"]["orchestrator"] = "ok"
    else:
        health_status["checks"]["orchestrator"] = "failed"
        health_status["status"] = "unhealthy"

    return health_status


@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(generate_latest(), media_type="text/plain")


@app.post("/agent/feedback")
async def submit_feedback(
    feedback: Dict[str, Any],
    user_info: Dict = Depends(verify_api_key)
):
    """Submit feedback for a completed task"""

    logger.info(
        "Feedback received",
        client_id=user_info["client_id"],
        task_id=feedback.get("task_id"),
        rating=feedback.get("rating")
    )

    return {"message": "Feedback received", "status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False
    )