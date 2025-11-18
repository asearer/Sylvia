# Use lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy camera and audio source code
COPY camera/src/ ./camera/src
COPY audio/src/ ./audio/src

# Install dependencies for both components
RUN pip install --no-cache-dir --upgrade pip \
    && pip install opencv-python-headless numpy sounddevice

# Set default working directory (camera by default, can change at runtime)
WORKDIR /app/camera/src

# Default command runs camera component
CMD ["python", "main.py"]

# To run audio component, override CMD at runtime:
# docker run <image_name> python ../audio/src/main.py
