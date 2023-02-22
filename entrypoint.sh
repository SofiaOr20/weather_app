#!/bin/sh
echo "Starting migrations for project..."
python /code/manage.py makemigrations
python /code/manage.py migrate --noinput
exec "$@"