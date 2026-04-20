FROM python:3.11-slim

# 1. Install Node.js (for npx) and build tools (for psycopg2/sqlalchemy)
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    gcc \
    python3-dev \
    libpq-dev \
    musl-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy source code
COPY . .

# 4. Config
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 5. Launch
CMD ["python", "graph.py"]
