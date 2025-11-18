# Base image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy source code
COPY src/ ./src

# Set working directory to src
WORKDIR /app/src

# Install dependencies placeholder
RUN pip install --no-cache-dir --upgrade pip

# Entrypoint
CMD ["python", "main.py"]
