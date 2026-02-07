
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    python3-dev \
    lsb-release \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

COPY services/voice_tts/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY libs /app/libs
COPY services/voice_tts /app/services/voice_tts

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "services/voice_tts/src/main.py"]
