.PHONY: build run docker-build docker-push deploy clean

# Build the operator binary
build:
	go build -o bin/operator main.go

# Run the operator locally
run: build
	./bin/operator

# Build the Docker image
docker-build:
	docker build -t basic-operator:latest .

# Push the Docker image (update registry as needed)
docker-push: docker-build
	docker push basic-operator:latest

# Deploy the CRD and operator to Kubernetes
deploy:
	kubectl apply -f crd.yaml
	kubectl apply -f deployment.yaml

# Clean up build artifacts
clean:
	rm -rf bin/

# Initialize go modules (run once)
init:
	go mod init basic-operator
	go mod tidy