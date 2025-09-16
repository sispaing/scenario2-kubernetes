#!/bin/bash

# This script cleans up all resources created by the setup script.
# It will delete the Minikube cluster, Kubernetes resources, and local Docker images.

echo "Starting cleanup process."

# --- 1. Uninstall Helm Chart and Namespaces ---
echo "Uninstalling Helm release and deleting namespaces."
# The '|| true' part ensures the script doesn't fail if the resources don't exist.
helm uninstall prometheus -n monitoring || true
kubectl delete namespace monitoring || true
kubectl delete namespace acp || true
echo "Helm release and namespaces have been deleted."

# --- 2. Delete Minikube Cluster ---
echo "Deleting Minikube cluster."
minikube delete --all --purge
echo "Minikube cluster has been deleted."

# --- 3. Remove Local Docker Images ---
echo "Removing application Docker images."
# Unset minikube's docker-env to connect to the system's docker daemon.
eval $(minikube docker-env -u) || true
docker rmi counter_app_backend:latest counter_app_frontend:latest || true
echo "Local Docker images have been removed."

echo "Cleanup complete."