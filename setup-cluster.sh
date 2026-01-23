#!/bin/bash
set -e

echo "Creating k3d cluster..."
k3d cluster create wiki \
    --api-port 6550 \
    --servers 1 \
    --agents 0 \
    --port "30080:30080@server:0" \
    --port "30081:30081@server:0" \
    --wait

echo "Waiting for cluster..."
kubectl wait --for=condition=ready node --all --timeout=120s

echo "Building wiki-service image..."
cd /app/wiki_service
docker build -t wiki-service:latest .

echo "Importing image to k3d..."
k3d image import wiki-service:latest -c wiki

echo "Installing Helm chart..."
cd /app
helm install wiki ./wiki-chart --wait --timeout=10m

echo "Waiting for pods..."
kubectl wait --for=condition=ready pod --all --timeout=600s

echo "Exposing services via NodePort..."
kubectl patch svc wiki-fastapi -p '{"spec":{"type":"NodePort","ports":[{"port":8000,"nodePort":30080,"targetPort":8000}]}}'
kubectl patch svc wiki-grafana -p '{"spec":{"type":"NodePort","ports":[{"port":3000,"nodePort":30081,"targetPort":3000}]}}'

echo "✅ Cluster deployment complete!"
kubectl get pods
kubectl get svc
