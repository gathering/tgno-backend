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
