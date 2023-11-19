# TG.no - Backend

**NB** Public repo, no secrets!

CMS and REST API built using [Wagtail](https://wagtail.org/). It runs on [http://localhost:8000](http://localhost:8000) by default. With admin pages exposed on [http://localhost:8000/admin](http://localhost:8000/admin)

For actual production usage we will most likely rely entierly on [REST API](https://docs.wagtail.org/en/stable/advanced_topics/api/v2/configuration.html), so consider all templates and html views test/dev only.

Initial site following structure as outlined in official [Getting Started tutorial](https://docs.wagtail.org/en/stable/getting_started/tutorial.html). So check that out for a quick introduction into how contents are structured.

## Current state

- Following Wagtail getting started tutorial
- `aktuelt` app is combination of `blog` from tutorial and start of actual Aktuelt section
- REST API requirements in place and certain routes exposed via `api.py` files (mapped in `tgno/urls.py`)
- `home` and `search` apps are init/tutorial leftovers

**Prioritized tasks:**

- Get local `docker-compose` based development setup functional and documented
- Get local editor tooling functional and documented
- Get staging environment up and running using terraform (in another repo for now)
- Limit sub-page types available on `aktuelt` app
- Start iterating on `aktuelt` app to get a minimal realistic and functional article setup in place  (look at existing page for inspiration)
- Iterate on README and other docs to include any relevant commands and setup steps

## Key Wagtail commands

Run this in docker container or locally, depending on your setup

**List all available commands**
```sh
python manage.py
```

**Migrate database**
```sh
python manage.py migrate
```

**Create new migrations after changing models**
```sh
# Create migrations
python manage.py makemigrations
# Optionally: Apply migrations if they look correct
python manage.py migrate
```

**Create new super (admin) user**
```sh
python manage.py createsuperuser
```

**Run site**
```sh
python manage.py runserver
```
