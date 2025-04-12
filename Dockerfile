FROM amazonlinux:2

# Set working directory
WORKDIR /build

# Install zip
RUN yum update -y && yum install -y zip

# Copy Lambda function
COPY workloads/aws/lambda_function.py .

# Create the zip directly
RUN zip function.zip lambda_function.py