
# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies if needed (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port (Firebase/Cloud Run sets PORT env var)
ENV PORT=8080

# Health check (optional, can be removed if causing issues)
# HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
#   CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT:-8080}/')" || exit 1

# Run the application
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}

