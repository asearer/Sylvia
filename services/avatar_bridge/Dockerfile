
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY services/avatar_bridge/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY libs /app/libs
COPY services/avatar_bridge /app/services/avatar_bridge

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "services/avatar_bridge/src/main.py"]
