# Shortcuts for development when using docker compose.
# Part documentation, part convenience
# 
# Whenever possible we recommend using an interactive shell inside of web
# container instead, since that gives full/easier access to any available
# Django or Wagtail commands
#
# This can be accessed by running: `docker compose exec web bash`
shell:
	docker compose exec web bash

makemigrations:
	docker compose exec web poetry run python manage.py makemigrations

migrate:
	docker compose exec web poetry run python manage.py migrate

createsuperuser:
	docker compose exec web poetry run python manage.py createsuperuser

mode = refresh
seed-for-development:
	docker compose exec web poetry run python manage.py seed --mode=$(mode)

# Run to trigger publishing of scheduled content when developing locally
# in production we run a cronjob that runs the wagtail command every x minutes
publish-scheduled:
	docker compose exec web poetry run python manage.py publish_scheduled


# Run to create a new app (aka. section) in the project
# Example: `make startapp name=blog`
startapp:
	docker compose exec web poetry run python manage.py startapp $(name)

tests:
	docker compose exec web poetry run python manage.py test

# Run tests with sqllite instead of postgres, mainly for CI purposes
ci-test:
	DATABASE_ENGINE=django.db.backends.sqlite3 poetry run python manage.py collectstatic
	DATABASE_ENGINE=django.db.backends.sqlite3 poetry run python manage.py test
