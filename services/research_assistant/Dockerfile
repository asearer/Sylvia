FROM python:3.11-slim

WORKDIR /app
COPY src/ ./src

# Install dependencies (placeholder, can add NLP libraries like nltk, transformers)
RUN pip install --no-cache-dir --upgrade pip

WORKDIR /app/src

CMD ["python", "main.py"]
