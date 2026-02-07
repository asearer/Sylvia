
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir streamlit redis

# Copy source code
COPY libs /app/libs
COPY apps/sylvia_app /app/apps/sylvia_app

# Set PYTHONPATH
ENV PYTHONPATH=/app

CMD ["streamlit", "run", "apps/sylvia_app/src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
