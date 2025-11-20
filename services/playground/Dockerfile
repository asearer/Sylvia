FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for py-mini-racer
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src ./src
COPY __init__.py ./

# Expose port
EXPOSE 5002

# Run the service using uvicorn with module path
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5002"]
