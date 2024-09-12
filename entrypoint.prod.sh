#!/bin/sh

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
    sleep 0.5
    echo "Waiting for PostgreSQL ($POSTGRES_HOST:$POSTGRES_PORT)"
done

python manage.py migrate --no-input
exec "$@"