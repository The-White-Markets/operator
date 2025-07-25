# Basic Operator MVP

A minimal Kubernetes operator that watches for custom resources and performs basic operations.

## Features
- Custom Resource Definition (CRD)
- Basic controller logic
- Simple reconciliation loop

## Components
- `main.go` - Entry point and controller setup
- `crd.yaml` - Custom Resource Definition
- `Dockerfile` - Container image build
- `Makefile` - Build and deployment commands