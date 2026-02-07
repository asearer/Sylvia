
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
# portaudio19-dev is needed for pyaudio
# flac and alsa-utils might be needed for speech recognition
RUN apt-get update && apt-get install -y \
    gcc \
    portaudio19-dev \
    python3-dev \
    flac \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

COPY services/voice_stt/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY libs /app/libs
COPY services/voice_stt /app/services/voice_stt

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["python", "services/voice_stt/src/main.py"]
