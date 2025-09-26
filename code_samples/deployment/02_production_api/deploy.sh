#!/bin/bash
# deploy.sh - One-click deployment script

set -e  # Exit on error

echo "🚀 Starting deployment process..."

# 1. Run tests (if test directory exists)
if [ -d "tests" ]; then
    echo "📝 Running tests..."
    pytest tests/ || { echo "❌ Tests failed"; exit 1; }
else
    echo "⚠️  No tests directory found, skipping tests"
fi

# 2. Build Docker image
echo "🔨 Building Docker image..."
docker build -t agent-api:latest .

# 3. Tag for registry (uncomment and modify for your registry)
# echo "🏷️  Tagging image..."
# docker tag agent-api:latest registry.railway.app/agent-api:latest

# 4. Push to registry (uncomment and modify for your registry)
# echo "📤 Pushing to registry..."
# docker push registry.railway.app/agent-api:latest

# 5. Deploy to cloud platform (uncomment and modify for your platform)
# echo "🚂 Deploying to Railway..."
# railway up --detach

# 6. For local deployment
echo "🏠 Starting local deployment..."
docker-compose up -d

# 7. Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# 8. Verify deployment
echo "✅ Verifying deployment..."
HEALTH_CHECK=$(curl -s http://localhost:8000/health | jq -r '.status' 2>/dev/null || echo "unhealthy")

if [ "$HEALTH_CHECK" = "healthy" ]; then
    echo "✨ Deployment successful!"
    echo "📍 API URL: http://localhost:8000"
    echo "📚 Docs: http://localhost:8000/docs"
    echo "🔍 Health: http://localhost:8000/health"
    echo "📊 Metrics: http://localhost:8000/metrics"
else
    echo "❌ Deployment verification failed"
    echo "🔍 Check logs with: docker-compose logs"
    exit 1
fi