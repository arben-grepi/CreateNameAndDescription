# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Expose port (Cloud Run sets PORT env var)
ENV PORT=8080

# Run the application
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8080}

