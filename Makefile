# Shortcuts for development when using docker-compose
# 
# Whenever possible we recommend using an interactive shell inside of web
# container instead, since that gives full/easier access to any available
# Django or Wagtail commands
#
# This can be accessed by running: `docker-compose exec web bash`
shell:
	docker-compose exec web bash

makemigrations:
	docker-compose exec web python manage.py makemigrations

migrate:
	docker-compose exec web python manage.py migrate

createsuperuser:
	docker-compose exec web python manage.py createsuperuser

# Run to trigger publishing of scheduled content when developing locally
# in production we run a cronjob that runs the wagtail command every x minutes
publish-scheduled:
	docker-compose exec web python manage.py publish_scheduled

test:
	docker-compose exec web python manage.py test

# Run tests with sqllite instead of postgres, mainly for CI purposes
ci-test:
	DATABASE_ENGINE=django.db.backends.sqlite3 python manage.py collectstatic
	DATABASE_ENGINE=django.db.backends.sqlite3 python manage.py test
