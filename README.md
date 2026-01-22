# Wiki Service Helm Chart

## Overview
Production-ready Helm chart for Wiki Service with FastAPI, PostgreSQL, Prometheus, and Grafana.

## Local Testing with Minikube
I tested this chart locally using Minikube.

- After deploying, I was able to access:
  - **Grafana** at [http://localhost:3000](http://localhost:3000) (after port-forwarding)
  - **FastAPI** user and post endpoints at [http://localhost:8000/users/](http://localhost:8000/users/) and [http://localhost:8000/posts/](http://localhost:8000/posts/) (after port-forwarding)

# Port forward FastAPI service
kubectl port-forward svc/wiki-fastapi 8000:8000

# In another terminal, port forward Grafana
kubectl port-forward svc/wiki-grafana 3000:3000

## Components
- FastAPI: Business logic layer
- PostgreSQL: Data persistence
- Prometheus: Metrics collection from /metrics endpoint
- Grafana: Dashboard visualization

## Directory Structure
```
/
├── wiki_service/
│   ├── Dockerfile
│   ├── main.py
│   └── requirements.txt
├── wiki-chart/
│   ├── Chart.yaml
│   ├── values.yaml
│   └── templates/
└── README.md
```

## Build Docker Image
```bash
cd wiki_service
docker build -t wiki-service:latest .
```

## Install Helm Chart
```bash
helm install wiki ./wiki-chart
```

## Access Services
```bash
# Port-forward Grafana
kubectl port-forward svc/<grafana-service-name> 3000:3000

# Port-forward FastAPI
kubectl port-forward svc/<fastapi-service-name> 8000:80
```

### Endpoints:
- **FastAPI**: http://localhost:8000/users/ and /posts/
- **Grafana**: http://localhost:3000
  - Username: admin
  - Password: admin

## Configuration
Change Docker image in values.yaml:
```yaml
fastapi:
  image_name: your-registry/wiki-service:v1.0.0
```

## Resource Requirements
- CPU: ~1.8 cores
- Memory: ~1.5GB RAM
- Disk: ~5GB

## Testing the API

### Create a User
```bash
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "email": "john@example.com"}'
```

### Create a Post
```bash
curl -X POST http://localhost:8000/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title": "My First Post", "content": "Hello World!", "user_id": 1}'
```

### View Metrics
```bash
curl http://localhost:8000/metrics
```

