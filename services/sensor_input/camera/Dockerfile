# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy source code
COPY src/ ./src

# Install dependencies (placeholder, add real packages as needed)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install opencv-python-headless numpy

# Set working directory to src
WORKDIR /app/src

# Entrypoint
CMD ["python", "main.py"]
