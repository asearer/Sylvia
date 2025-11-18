FROM python:3.11-slim

WORKDIR /app
COPY src/ ./src

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install opencv-python-headless numpy

WORKDIR /app/src

CMD ["python", "main.py"]
, "-b"]