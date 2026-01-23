#!/bin/bash
set -e

echo "=========================================="
echo "Starting Docker-in-Docker k3d Cluster"
echo "=========================================="

dockerd-entrypoint.sh &

echo "Waiting for Docker daemon..."
for i in {1..60}; do
    if docker info >/dev/null 2>&1; then
        echo "✅ Docker daemon ready"
        break
    fi
    sleep 1
done

/setup-cluster.sh

echo "Starting nginx proxy..."
nginx

echo "=========================================="
echo "✅ ALL SERVICES READY!"
echo "=========================================="
echo ""
echo "Access the following endpoints:"
echo "  • FastAPI Users:  http://localhost:8080/users/"
echo "  • FastAPI Posts:  http://localhost:8080/posts/"
echo "  • Grafana:        http://localhost:8080/grafana/d/creation-dashboard-678/creation"
echo "                    Login: admin / admin"
echo ""
echo "Test with:"
echo '  curl -X POST http://localhost:8080/users/ -H "Content-Type: application/json" -d '"'"'{"username":"test","email":"test@example.com"}'"'"
echo ""
echo "=========================================="

tail -f /dev/null
