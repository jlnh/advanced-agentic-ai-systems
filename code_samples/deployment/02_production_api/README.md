# Production Multi-Agent System API

A production-ready FastAPI application for AI agent orchestration with authentication, rate limiting, caching, and monitoring capabilities.

## 📋 Overview

This project provides a complete production API that transforms local AI agents into a scalable, secure web service. It includes:

- **FastAPI** application with automatic OpenAPI documentation
- **Redis** for distributed rate limiting and caching
- **Authentication** via API keys
- **Rate limiting** per client
- **Health checks** and monitoring
- **Prometheus metrics** export
- **Docker** containerization
- **Security features** including prompt injection protection

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Redis (included in docker-compose)

### 1. Clone and Setup

```bash
# Navigate to the project directory
cd /path/to/this/directory

# Copy environment configuration
cp .env.example .env

# Edit .env with your API keys
nano .env
```

### 2. Environment Setup

Edit the `.env` file with your configuration:

```bash
# Required for agent functionality
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: For enhanced tracing
LANGCHAIN_API_KEY=ls-your-langchain-api-key-here

# API security (comma-separated)
API_KEYS=your-secure-api-key-1,your-secure-api-key-2

# CORS settings
ALLOWED_ORIGINS=http://localhost:3000,https://yourdomain.com
```

### 3. Run with Docker Compose (Recommended)

```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### 4. Alternative: Local Python Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Redis (separate terminal)
redis-server

# Run the API
python main.py
```

## 📖 API Documentation

Once running, access the interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health
- **Metrics**: http://localhost:8000/metrics

## 🔑 API Usage

### Authentication

All requests require a Bearer token in the Authorization header:

```bash
curl -X POST "http://localhost:8000/agent/execute" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Summarize the benefits of FastAPI",
    "agent_type": "general"
  }'
```

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/agent/execute` | Execute agent task (sync/async) |
| GET | `/agent/status/{task_id}` | Check async task status |
| POST | `/agent/feedback` | Submit task feedback |
| GET | `/health` | Health check |
| GET | `/metrics` | Prometheus metrics |

### Request Examples

#### Synchronous Execution
```python
import requests

response = requests.post(
    "http://localhost:8000/agent/execute",
    headers={"Authorization": "Bearer your-api-key"},
    json={
        "task": "Explain machine learning in simple terms",
        "agent_type": "general",
        "context": {"audience": "beginner"},
        "async_execution": False
    }
)

print(response.json())
```

#### Asynchronous Execution
```python
# Submit task
response = requests.post(
    "http://localhost:8000/agent/execute",
    headers={"Authorization": "Bearer your-api-key"},
    json={
        "task": "Research the latest AI developments",
        "agent_type": "research",
        "async_execution": True
    }
)

task_id = response.json()["task_id"]

# Check status later
status = requests.get(
    f"http://localhost:8000/agent/status/{task_id}",
    headers={"Authorization": "Bearer your-api-key"}
)

print(status.json())
```

## 🧪 Testing

### Run the Test Suite

```bash
# Test the API endpoints
python test_api.py

# Or with explicit Python path
python3 test_api.py
```

The test script will validate:
- Health checks
- Authentication
- Synchronous execution
- Asynchronous execution
- Rate limiting
- Metrics endpoint

### Manual Testing

```bash
# Health check
curl http://localhost:8000/health

# Test with valid API key
curl -X POST "http://localhost:8000/agent/execute" \
  -H "Authorization: Bearer demo-key-123" \
  -H "Content-Type: application/json" \
  -d '{"task": "Hello world test"}'

# Test rate limiting (run multiple times quickly)
for i in {1..15}; do
  curl -X POST "http://localhost:8000/agent/execute" \
    -H "Authorization: Bearer demo-key-123" \
    -H "Content-Type: application/json" \
    -d '{"task": "Rate limit test '$i'"}' &
done
```

## 📊 Monitoring and Observability

### Health Checks

The `/health` endpoint provides comprehensive system status:

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.0.0",
  "checks": {
    "redis": "ok",
    "orchestrator": "ok"
  }
}
```

### Metrics

Prometheus metrics are available at `/metrics`:

- `agent_requests_total`: Total number of requests
- `agent_request_duration_seconds`: Request processing time

### Structured Logging

All operations are logged with structured data:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "info",
  "event": "agent_task_started",
  "task_id": "uuid-here",
  "client_id": "client_0",
  "task_type": "general"
}
```

## 🛡️ Security Features

### Authentication
- Bearer token authentication
- Hashed API key storage
- Per-client access control

### Rate Limiting
- Redis-backed distributed rate limiting
- Configurable limits per client tier
- Automatic reset windows

### Input Validation
- Pydantic models for request validation
- Prompt injection detection
- Input length and character limits

### Security Headers
- CORS configuration
- Timeout controls
- Request size limits

## 🐳 Deployment

### Local Development

```bash
# Start with hot reload
docker-compose up --build

# View logs
docker-compose logs -f api
```

### Production Deployment

1. **Build Production Image**
   ```bash
   docker build -t agent-api:production .
   ```

2. **Deploy to Cloud Platform**
   - **Railway**: `railway up`
   - **Render**: Connect your repo
   - **Fly.io**: `fly deploy`
   - **AWS ECS/Fargate**: Use provided Dockerfile

3. **Environment Variables**
   Set these in your cloud platform:
   ```
   OPENAI_API_KEY=sk-...
   API_KEYS=prod-key-1,prod-key-2
   REDIS_URL=redis://your-redis-instance
   ALLOWED_ORIGINS=https://yourdomain.com
   ```

### Deployment Script

Use the included deployment script:

```bash
# Make executable (if not already)
chmod +x deploy.sh

# Deploy locally
./deploy.sh
```

## 📁 Project Structure

```
production-api/
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container configuration
├── docker-compose.yml  # Local development setup
├── deploy.sh           # Deployment script
├── test_api.py         # API test suite
├── .env.example        # Environment template
└── README.md           # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | Yes |
| `API_KEYS` | Comma-separated API keys | demo-key-123 | Yes |
| `REDIS_URL` | Redis connection URL | redis://localhost:6379 | No |
| `ALLOWED_ORIGINS` | CORS allowed origins | * | No |
| `PORT` | Server port | 8000 | No |
| `DEFAULT_RATE_LIMIT` | Requests per window | 10 | No |
| `RATE_LIMIT_WINDOW` | Rate limit window (seconds) | 60 | No |

### Rate Limiting Tiers

- **Basic**: 10 requests/minute
- **Premium**: 100 requests/minute
- Custom limits can be configured per API key

## 🔧 Development

### Adding New Endpoints

1. Define request/response models:
   ```python
   class MyRequest(BaseModel):
       field: str
   ```

2. Add endpoint function:
   ```python
   @app.post("/my-endpoint")
   async def my_endpoint(request: MyRequest, user_info=Depends(verify_api_key)):
       # Implementation
       pass
   ```

3. Add tests to `test_api.py`

### Extending Agent Functionality

The current implementation uses a `MockOrchestrator`. To integrate real agents:

1. Replace `MockOrchestrator` in `main.py`
2. Import your agent orchestration system
3. Update the `initialize_orchestrator()` function

### Custom Middleware

Add middleware for additional functionality:

```python
@app.middleware("http")
async def custom_middleware(request, call_next):
    # Custom logic
    response = await call_next(request)
    return response
```

## 🚨 Troubleshooting

### Common Issues

1. **Redis Connection Failed**
   ```bash
   # Start Redis locally
   redis-server

   # Or use Docker
   docker run -d -p 6379:6379 redis:alpine
   ```

2. **Port Already in Use**
   ```bash
   # Change port in .env
   PORT=8001

   # Or kill existing process
   lsof -ti:8000 | xargs kill -9
   ```

3. **Authentication Errors**
   - Check API key in `.env`
   - Ensure Bearer token format: `Bearer your-key`

4. **Rate Limit Issues**
   ```bash
   # Clear Redis rate limit data
   redis-cli FLUSHDB
   ```

### Debug Mode

Enable debug logging:

```bash
LOG_LEVEL=DEBUG python main.py
```

## 📈 Performance Targets

The API is designed to achieve:

- **Response time**: p95 < 10 seconds
- **Availability**: >99.5% uptime
- **Error rate**: <1% of requests
- **Throughput**: 100+ requests/minute
- **Cost**: <$0.50 per request average

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📄 License

This project is part of the Advanced Agentic AI Systems course materials.

## 📚 Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Redis Documentation](https://redis.io/documentation)
- [Docker Compose Guide](https://docs.docker.com/compose/)
- [API Security Best Practices](https://owasp.org/www-project-api-security/)

---

For questions or support, refer to the course materials or create an issue in the repository.