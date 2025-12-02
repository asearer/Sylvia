FROM python:3.11-slim
WORKDIR /app

# Copy requirements for the app
COPY apps/sylvia_app/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app and services (since app imports services)
COPY apps/sylvia_app/src ./src
COPY services ./services

# Ensure python path includes root
ENV PYTHONPATH=/app

EXPOSE 5000
CMD ["streamlit", "run", "src/main.py", "--server.port=5000", "--server.address=0.0.0.0"]
