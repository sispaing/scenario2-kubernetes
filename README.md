# ACP Project - Counter Application On Local Kubernetes Cluster

This project demonstrates a counter application built with modern containerization and orchestration technologies. It showcases deployment patterns using both Docker Compose and Kubernetes.

## Project Overview

The ACP (Application Container Platform) project contains a full-stack counter application that demonstrates:
- Microservices architecture
- Container orchestration
- Database persistence


## Architecture

The application consists of three main components:

### Frontend
- **Technology**: HTML, CSS, JavaScript with Nginx
- **Port**: 8080 (Docker Compose) / 80 (Kubernetes)
- **Description**: Simple web interface with increment/decrement buttons

### Backend
- **Technology**: Python Flask with CORS support
- **Port**: 5000
- **Description**: REST API providing counter operations
- **Endpoints**:
  - `GET /api/counter` - Get current counter value
  - `POST /api/counter/increment` - Increment counter
  - `POST /api/counter/decrement` - Decrement counter

### Database
- **Technology**: MySQL 8.0
- **Port**: 3306
- **Description**: Persistent storage for counter values
- **Database**: `counter_db`
- **Table**: `counter` with auto-incrementing ID and timestamp

## Project Structure

```
scenario2-kubernetes/
├── README.md
├── cleanup.sh
├── counter_app
│   ├── README.md
│   ├── backend
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── docker-compose.yaml
│   ├── frontend
│   │   ├── Dockerfile
│   │   ├── api-connector.js
│   │   ├── index.html
│   │   ├── nginx.conf
│   │   ├── script.js
│   │   └── style.css
│   ├── k8s
│   │   ├── backend.yaml
│   │   ├── frontend.yaml
│   │   └── mysql.yaml
│   └── script.js
├── setup.sh
```

## Prerequisites

### For Docker Compose Deployment
- Docker
- Docker Compose

### For Kubernetes Deployment
- Minikube
- kubectl
- Docker (for building images)

## Quick Start

### 1. Environment Setup

Run the setup script to install Minikube and kubectl (Linux):
```bash
chmod +x setup.sh
./setup.sh
```

### 2. Docker Compose Deployment

Navigate to the counter_app directory and start the application:
```bash
cd counter_app
docker-compose up --build
```

Access the application at: http://localhost:8080

### 3. Kubernetes Deployment

Build the Docker images:
```bash
cd counter_app
docker build -t counter_app_backend:latest ./backend
docker build -t counter_app_frontend:latest ./frontend
```

Load images into Minikube:
```bash
minikube image load counter_app_backend:latest
minikube image load counter_app_frontend:latest
```

Create namespace and deploy:
```bash
kubectl create namespace acp
kubectl apply -f k8s/
```

Access the application:
```bash
minikube service frontend -n acp
```

## Monitoring and Debugging

### Check Container Logs (Docker Compose)
```bash
docker logs -f counter_app-backend-1
docker logs -f counter_app-frontend-1
docker logs -f counter_app-mysql-1
```

### Check Database Values
**Docker Compose:**
```bash
docker compose exec mysql mysql -u root -p'rootpassword' -e 'SELECT value FROM counter_db.counter ORDER BY id DESC LIMIT 1;'
```

**Kubernetes:**
```bash
kubectl exec -it mysql-0 -n acp -- mysql -u root -p'rootpassword' -e 'SELECT value FROM counter_db.counter ORDER BY id DESC LIMIT 1;'
```

### Kubernetes Debugging
```bash
# Check pod status
kubectl get pods -n acp

# Check service status
kubectl get services -n acp

# View pod logs
kubectl logs -f deployment/backend-deployment -n acp
kubectl logs -f deployment/frontend-deployment -n acp
```

## Features

- **Persistent Counter**: Counter values are stored in MySQL database
- **Health Checks**: Database health checks ensure proper startup order
- **CORS Support**: Frontend can communicate with backend across different origins
- **Auto-scaling Ready**: Kubernetes deployment supports horizontal pod autoscaling
- **Namespace Isolation**: Kubernetes resources are deployed in dedicated `acp` namespace

## Development

### Local Development
1. Start MySQL database: `docker-compose up mysql`
2. Run backend: `cd backend && python app.py`
3. Serve frontend: Use any HTTP server for the frontend directory

### Building Images
```bash
# Backend
docker build -t counter_app_backend:latest ./backend

# Frontend  
docker build -t counter_app_frontend:latest ./frontend
```

## Troubleshooting

### Common Issues
1. **Database Connection Failed**: Ensure MySQL container is healthy before starting backend
2. **Frontend Can't Reach Backend**: Check configuration and network connectivity
3. **Kubernetes ImagePullBackOff**: Ensure images are loaded into Minikube with `minikube image load`

### Port Conflicts
- Docker Compose uses ports 3306, 5000, and 8080
- Ensure these ports are available on your system

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with both Docker Compose and Kubernetes
5. Submit a pull request

