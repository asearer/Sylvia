FROM python:3.11-slim
WORKDIR /app
COPY src/ ./src
COPY ../../libs/ ./libs/
COPY requirements.txt ./
ENV PYTHONPATH="${PYTHONPATH}:/app/libs"
RUN pip install matrix-nio[http]
CMD ["python", "src/bot.py"]
