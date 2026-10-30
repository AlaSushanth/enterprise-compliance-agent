FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete project codebase
COPY . .

# Expose FastAPI port
EXPOSE 8000

ENV PYTHONUNBUFFERED=1

CMD ["python", "run.py"]
