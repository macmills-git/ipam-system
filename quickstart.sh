#!/bin/bash
# IPAM System Quick Start Script

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║         IPAM System - Quick Start Installation            ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker found: $(docker --version)"
echo "✅ Docker Compose found: $(docker-compose --version)"
echo ""

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
else
    echo "✅ .env file already exists"
fi

echo ""
echo "Starting IPAM system..."
echo "This may take a few minutes on first run..."
echo ""

# Start services
docker-compose up -d --build

echo ""
echo "Waiting for services to be ready..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║              🎉 IPAM System is Ready! 🎉                  ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "📱 Access the application:"
    echo "   Frontend:  http://localhost:3000"
    echo "   API:       http://localhost:8000"
    echo "   Swagger:   http://localhost:8000/docs"
    echo "   Grafana:   http://localhost:3001 (admin/admin)"
    echo ""
    echo "🔐 Default credentials:"
    echo "   Email:     admin@ipam.local"
    echo "   Password:  Admin123!"
    echo ""
    echo "📚 Documentation:"
    echo "   README:    ./README.md"
    echo "   API Docs:  ./docs/API.md"
    echo "   Deploy:    ./docs/DEPLOYMENT.md"
    echo ""
    echo "🛠️  Useful commands:"
    echo "   View logs:     docker-compose logs -f"
    echo "   Stop system:   docker-compose down"
    echo "   Restart:       docker-compose restart"
    echo "   Run tests:     cd backend && pytest"
    echo ""
    echo "⚠️  Remember to change default passwords in production!"
    echo ""
else
    echo "❌ Some services failed to start. Check logs with:"
    echo "   docker-compose logs"
    exit 1
fi
