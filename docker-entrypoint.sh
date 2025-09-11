#!/bin/sh
set -e

wait_for_db() {
  echo "Waiting for database to become available..."
  while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
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