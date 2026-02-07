# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy service files
COPY . /app

# Install dependencies if present
# (Keeps things optional so the service doesn't break if empty)
RUN if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi

# Default command (runs the data service API)
CMD ["python", "main.py"]
