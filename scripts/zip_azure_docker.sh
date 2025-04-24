#!/bin/bash

set -e

echo "=== Building function.zip for Azure Functions using Docker ==="

# Build the image
docker build -t azure_function_builder -f Dockerfile.azure .

# Remove any previous container
docker rm -f azure_function_container 2>/dev/null || true

# Run container to generate zip
docker run --name azure_function_container azure_function_builder

# Copy the zip out
docker cp azure_function_container:/build/function.zip workloads/azure/

# Cleanup container
docker rm azure_function_container

echo "Success: function.zip created at workloads/azure"