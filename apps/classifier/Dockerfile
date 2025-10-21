FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src
COPY requirements.txt ./
# Copy libs from the project root (one directory above classifier)
COPY ../libs/ ./libs/
ENV PYTHONPATH="${PYTHONPATH}:/app/libs"
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "src/train.py"]
