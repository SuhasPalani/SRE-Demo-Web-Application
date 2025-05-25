#!/bin/bash
# Setup script for development environment

echo "🔧 Setting up SRE Demo environment..."

# Create necessary directories
mkdir -p logs config dashboards

# Create .gitkeep for logs directory
touch logs/.gitkeep

# Create default config
cat > config/monitor_config.yml << EOF
targets:
  - name: webapp
    url: http://webapp:5000/health
    timeout: 5
    expected_status: 200
  - name: webapp_metrics
    url: http://webapp:5000/metrics
    timeout: 5
    expected_status: 200

thresholds:
  consecutive_failures: 3
  response_time_ms: 2000

remediation:
  enabled: true
  restart_service: true

alerts:
  enabled: true
  channels:
    - console
    - file
EOF

echo "📝 Created default configuration"

# Check Docker installation
if ! command -v docker &> /dev/null; then
    echo "⚠️  Docker is not installed. Please install Docker first:"
    echo "   Ubuntu/Debian: sudo apt-get install docker.io docker-compose"
    echo "   macOS: Install Docker Desktop"
    echo "   Windows: Install Docker Desktop"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "⚠️  Docker Compose is not installed. Installing..."
    if command -v pip3 &> /dev/null; then
        pip3 install docker-compose
    else
        echo "Please install docker-compose manually"
        exit 1
    fi
fi

echo "✅ Setup completed!"
echo ""
echo "Next steps:"
echo "1. Run './scripts/deploy.sh' to start the demo"
echo "2. Check 'docker-compose ps' to see running services"
echo "3. Monitor with 'docker-compose logs -f monitor'"