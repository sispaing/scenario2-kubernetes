#!/bin/bash
# This script installs tools, builds images, and deploys the entire application stack.

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting the setup process."

# --- 1. Install Required Tools ---
echo "Checking for and installing required tools."

# Install Docker if not already installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found. Installing Docker."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
    echo "Docker has been installed."
    echo "IMPORTANT: Please open a new terminal and re-run this script for user permissions to apply."
    exit 1
fi

# Install Minikube if not already installed
if ! command -v minikube &> /dev/null; then
    echo "Minikube not found. Installing..."
    curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
    sudo install minikube /usr/local/bin/
    rm minikube
fi

# Install kubectl if not already installed
if ! command -v kubectl &> /dev/null; then
    echo "kubectl not found. Installing..."
    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    sudo install -o root -g root -m 0755 kubectl /usr/local/bin/
    rm kubectl
fi

# Install Helm if not already installed
if ! command -v helm &> /dev/null; then
    echo "Helm not found. Installing..."
    sudo snap install helm --classic
fi

echo "All required tools are installed."

# --- 2. Start Minikube & Configure Environment ---
echo "Starting Minikube."
minikube start --driver=docker

echo "Setting Docker to use Minikube's environment."
eval $(minikube docker-env)
echo "Minikube is running and configured."

# --- 3. Build Application Docker Images ---
echo "Building backend and frontend Docker images."
docker build -t counter_app_backend:latest ./counter_app/backend/
docker build -t counter_app_frontend:latest ./counter_app/frontend/
echo "Application images have been built."

# --- 4. Deploy Application and Monitoring Stack ---
echo "Deploying application and monitoring stack."
echo "Creating 'acp' namespace for the application."
kubectl create namespace acp

echo "Applying application manifests."
kubectl apply -f ./counter_app/k8s/

echo "Installing Prometheus monitoring stack."
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace
echo "Deployments have been initiated. Waiting for all pods to be ready."

# --- 5. Wait for Pods to be Ready ---
echo "Waiting for application pods in the 'acp' namespace..."
kubectl wait --for=condition=Ready pods --all -n acp --timeout=300s

echo "Waiting for monitoring pods in the 'monitoring' namespace..."
kubectl wait --for=condition=Ready pods --all -n monitoring --timeout=600s

echo "All services are up and running."

# --- 6. Final Instructions ---
GRAFANA_PASS=$(kubectl get secret --namespace monitoring prometheus-grafana -o jsonpath="{.data.admin-password}" | base64 --decode)

echo "Setup Complete. You can now access the services."
echo ""
echo "Grafana Dashboard:"
echo "  In a new terminal, run: kubectl port-forward --namespace monitoring svc/prometheus-grafana 3000:80"
echo "  Access URL: http://localhost:3000"
echo "  User: admin"
echo "  Password: ${GRAFANA_PASS}"
echo ""
echo "Counter Application:"
echo "  In a new terminal, run: minikube service -n acp frontend"