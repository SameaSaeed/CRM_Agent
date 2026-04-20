FROM postgres:15-alpine

# 1. Install system dependencies
RUN apk add --no-cache python3 py3-pip g++ gcc postgresql-dev python3-dev musl-dev
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 2. Set the working directory FIRST
WORKDIR /app

# 3. Copy the SQL file specifically using the relative path from the context

COPY *.sql /docker-entrypoint-initdb.d/

# 4. Copy and install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy everything else into /app
COPY . .
