#!/bin/bash
# Deployment script for SRE demo using Docker Compose V2

set -euo pipefail

echo "🚀 Deploying SRE Demo Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if Docker Compose V2 is available
if ! docker compose version > /dev/null 2>&1; then
    echo "❌ Docker Compose V2 is required. Run: 'docker compose version' to verify."
    echo "👉 Try using 'docker compose' instead of 'docker-compose'."
    exit 1
fi

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
docker compose down --remove-orphans || true

# Build and start services
echo "🔨 Building services..."
docker compose build --no-cache

echo "🚀 Starting services..."
docker compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for WebApp to become healthy..."
sleep 10

max_attempts=10
attempt=1

until curl -fs http://localhost:5000/health > /dev/null 2>&1 || [ $attempt -gt $max_attempts ]; do
    echo "⏳ Attempt $attempt/$max_attempts: WebApp not ready yet..."
    sleep 5
    attempt=$((attempt + 1))
done

if [ $attempt -gt $max_attempts ]; then
    echo "❌ WebApp health check failed after $max_attempts attempts"
    echo "📋 Container logs:"
    docker compose logs webapp
    exit 1
fi

echo "✅ WebApp is healthy!"
echo ""
echo "✅ Deployment completed successfully!"
echo ""
echo "🌐 Application URLs:"
echo "   WebApp:     http://localhost:5000"
echo "   Health:     http://localhost:5000/health"
echo "   Metrics:    http://localhost:5000/metrics"
echo ""
echo "📊 Monitoring Commands:"
echo "   View logs:  docker compose logs -f monitor"
echo "   All logs:   docker compose logs -f"
echo "   Status:     docker compose ps"
echo ""
echo "🧪 Test Commands:"
echo "   Crash test: curl http://localhost:5000/crash"
echo "   Health:     curl http://localhost:5000/health"
