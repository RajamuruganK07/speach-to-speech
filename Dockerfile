FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libsndfile1-dev \
    portaudio19-dev \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create models directory
RUN mkdir -p models

# Expose port (if needed for web interface)
EXPOSE 8000

# Default command
CMD ["python", "main.py"]