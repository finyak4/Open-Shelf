# Stage 1: build dependencies
FROM python:3.11-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -q && \
    apt-get install -y -q --no-install-recommends \
        build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2: production image
FROM python:3.11-slim


ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
# Install system dependencies
RUN apt-get update -q && \
    apt-get install -y -q --no-install-recommends \
        netcat-openbsd postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Copy entrypoint script and make it executable
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Expose the port Django will run on
EXPOSE 8000

# Use the entrypoint script as the container's entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["gunicorn", "library_ms.wsgi:application", "--bind=0.0.0.0:8000", "--workers=3", "--timeout=120"]