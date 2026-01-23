## Part1

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



# Wiki Service - Part1 and Part2

## Quick Start

### 1. Build

docker build -t wiki-dind:latest .

### 2. Run
docker run -d \
    --name wiki-dind \
    --privileged \
    -p 8080:8080 \
    wiki-dind:latest

### 4. Test (after 2-3 minutes)

1. Health check:

curl -s http://localhost:8080/health

2. Creating a user:

curl -s -X POST http://localhost:8080/users/ \
    -H "Content-Type: application/json" \
    -d '{"username":"alice","email":"alice@example.com"}'

3. Listing users:
curl -s http://localhost:8080/users/

4. Creating a post:

curl -s -X POST http://localhost:8080/posts/ \
    -H "Content-Type: application/json" \
    -d '{"title":"First Post","content":"Hello World!","user_id":1}'

5. Listing posts:

curl -s http://localhost:8080/posts/ 

6. Access Grafana at:
 http://localhost:8080/grafana/d/creation-dashboard-678/creation"
 Login: admin / admin"


## Access Points

- **FastAPI Users**: http://localhost:8080/users/
- **FastAPI Posts**: http://localhost:8080/posts/
- **Grafana Dashboard**: http://localhost:8080/grafana/d/creation-dashboard-678/creation
  - Username: `admin`
  - Password: `admin`

## Example Usage

```bash
# Create a user
curl -X POST http://localhost:8080/users/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john","email":"john@example.com"}'

# Create a post
curl -X POST http://localhost:8080/posts/ \
  -H "Content-Type: application/json" \
  -d '{"title":"My Post","content":"Hello!","user_id":1}'

# List users
curl http://localhost:8080/users/

# List posts
curl http://localhost:8080/posts/
```

## Troubleshooting

If you get 404 errors:
1. Wait longer (3-5 minutes for full startup)
2. Check logs: `docker logs wiki-dind`
3. Verify services are running: `docker exec wiki-dind kubectl get pods`
