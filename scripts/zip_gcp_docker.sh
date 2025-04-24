#!/bin/bash

set -e

echo "=== Building function.zip for Google Cloud Functions using Docker ==="

# Build the image
docker build -t gcf_builder -f Dockerfile.gcp .

# Remove any previous container
docker rm -f gcf_container 2>/dev/null || true

# Run container to generate zip
docker run --name gcf_container gcf_builder

# Copy the zip out
docker cp gcf_container:/build/function.zip workloads/gcp/

# Cleanup container
docker rm gcf_container

echo "Success: function.zip created at workloads/gcp"