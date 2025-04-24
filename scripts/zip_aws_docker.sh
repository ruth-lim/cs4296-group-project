#!/bin/bash

set -e

echo "=== Building function.zip using Docker ==="

# Build the image
docker build -t lambda_builder .

# Remove any previous container
docker rm -f lambda_container 2>/dev/null || true

# Run container to generate zip
docker run --name lambda_container lambda_builder

# Copy the zip out
docker cp lambda_container:/build/function.zip workloads/aws/

# Cleanup container
docker rm lambda_container

echo "Succss: function.zip created at workloads/aws"