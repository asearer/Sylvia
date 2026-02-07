
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# portaudio19-dev is needed for pyaudio
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY services/agent_core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY libs /app/libs
COPY services/agent_core /app/services/agent_core

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "services/agent_core/src/main.py"]
