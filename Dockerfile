FROM python:3.11-slim

# Environment setup
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update -q && \
    apt-get install -y -q --no-install-recommends \
        build-essential libpq-dev netcat-openbsd postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# EXPOSE 8000

# Entrypoint and command
ENTRYPOINT ["/docker-entrypoint.sh"]
# CMD ["gunicorn", "library_core.wsgi:application", "--bind=0.0.0.0:8000", "--workers=3", "--timeout=120"]  LOCAL
CMD gunicorn library_core.wsgi:application --bind=0.0.0.0:$PORT --workers=3 --timeout=120 # PROD for Render.com