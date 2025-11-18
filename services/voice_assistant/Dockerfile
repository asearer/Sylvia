FROM python:3.11-slim

WORKDIR /app
COPY src/ ./src
WORKDIR /app/src
RUN pip install --no-cache-dir --upgrade pip

CMD ["python", "main.py"]
