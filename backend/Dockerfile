# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /app

# Copy only requirements first (caching optimization)
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY backend /app/backend

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI using Uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

