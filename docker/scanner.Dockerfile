FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for network scanning
RUN apt-get update && apt-get install -y \
    iputils-ping \
    netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Copy scanner code
COPY scanner-agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scanner-agent/ .

# Run scanner
CMD ["python", "scanner.py"]
