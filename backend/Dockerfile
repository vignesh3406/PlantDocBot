FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY . .

# Create models directory (model will be downloaded at startup from HuggingFace)
RUN mkdir -p models

# Expose port (Render sets $PORT dynamically)
EXPOSE 8000

# Start the FastAPI app
# Render sets PORT env var; default to 8000 for local testing
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
