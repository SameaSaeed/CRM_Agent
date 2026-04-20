# Use a slim Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for some python packages)
RUN apt-get update && apt-get install -y gcc g++ && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your frontend code
# Make sure the 'ralph' folder is also copied if it's in this directory
COPY . .

# Run the script
# We use -u to force unbuffered output so you see logs in real-time
CMD ["python", "-u", "chat_local.py"]
