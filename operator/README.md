# Basic Kubernetes Operator MVP

A minimal Kubernetes operator that watches for `MyResource` custom resources and performs basic reconciliation.

## Features

- Custom Resource Definition (CRD) for `MyResource`
- Basic controller that watches for resource changes
- Simple reconciliation loop that updates resource status
- Kubernetes RBAC configuration
- Docker containerization

## Quick Start

### 1. Deploy the CRD
```bash
kubectl apply -f crd.yaml
```

### 2. Build and Deploy the Operator
```bash
# Build the operator
make build

# Build Docker image
make docker-build

# Deploy to Kubernetes
make deploy
```

### 3. Create a Test Resource
```bash
kubectl apply -f example-resource.yaml
```

### 4. Check the Status
```bash
kubectl get myresources
kubectl describe myresource example-myresource
```

## Development

### Local Development
```bash
# Run operator locally (requires kubeconfig)
make run
```

### Building
```bash
# Build binary
make build

# Build Docker image
make docker-build
```

## File Structure

- `main.go` - Main operator logic with controller and reconciliation
- `crd.yaml` - Custom Resource Definition
- `deployment.yaml` - Kubernetes deployment with RBAC
- `example-resource.yaml` - Example MyResource for testing
- `Dockerfile` - Container image build
- `Makefile` - Build and deployment commands

## How It Works

1. The operator watches for `MyResource` custom resources
2. When a resource is created/modified, it triggers reconciliation
3. The reconciler reads the resource spec and updates the status
4. Status includes phase, message, and last updated timestamp

This is a minimal MVP - extend as needed for your specific use case!