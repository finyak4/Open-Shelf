#!/bin/sh
set -e

# For local development
# wait_for_db() {
#   echo "Waiting for database to become available..."
#   while ! pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER"; do
#     sleep 1
#   done
#   echo "Database is available!"
# }  

# For production (e.g., Render.com)

wait_for_db() {
  echo "Waiting for database to become available..."
  echo "DATABASE_URL is: $DATABASE_URL"
  DB_HOST=$(python3 -c "import os; from urllib.parse import urlparse; u=urlparse(os.environ['DATABASE_URL']); print(u.hostname)")
  DB_PORT=$(python3 -c "import os; from urllib.parse import urlparse; u=urlparse(os.environ['DATABASE_URL']); print(u.port)")
  echo "DB_HOST is: $DB_HOST"
  echo "DB_PORT is: $DB_PORT"
  while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" > /dev/null 2>&1; do
    sleep 1
  done
  echo "Database is available!"
}

echo "Collecting static files..."
python manage.py collectstatic --noinput

if echo "$@" | grep -q "gunicorn"; then
    wait_for_db
    echo "Running database migrations..."
    python manage.py migrate
    echo "Starting Gunicorn..."
fi

exec "$@"