#!/bin/bash
echo "Running ./entrypoint.dev.sh"

echo "Validating main assumptions"
if [ ! -f ./manage.py ]; then
    echo "No manage.py file detected! Have the app code volume been mounted in docker-compose.yml file? This is required for dev image usage"
	exit 1
fi

echo "Refreshing poetry install"
poetry install

echo "Activating poetry env"
eval $(poetry env activate)

echo "Collecting static files"
python manage.py collectstatic --noinput --clear

echo "Checking for pending migrations (not applying)"
python manage.py migrate --plan

exec "$@"
