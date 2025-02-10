# TG.no - Backend

**NB** Public repo. So avoid pushing secrets...

CMS and REST API built using [Wagtail](https://wagtail.org/). It runs on [http://localhost:8000](http://localhost:8000) by default. With admin pages exposed on [http://localhost:8000/admin](http://localhost:8000/admin) and API exposed at [http://localhost:8000/api/v2/](http://localhost:8000/api/v2/)

For actual production usage we will most likely rely entierly on [REST API](https://docs.wagtail.org/en/stable/advanced_topics/api/v2/configuration.html), so consider all templates and html views test/dev only.

Initial site following structure as outlined in official [Getting Started tutorial](https://docs.wagtail.org/en/stable/getting_started/tutorial.html). So check that out for a quick introduction into how contents are structured.

Example urls
- [Aktuelt / News API](http://localhost:8000/api/v2/news/)
- [Aktuelt section / news page](http://localhost:8000/aktuelt/)

## Getting started

### 1. Get things up and running locally

We are mainly using Docker via docker-compose for local development (using poetry for dependency management inside the `web` container). To get started

1. Copy `.env.example` to `.env`
2. Start apps via `docker compose up`
3. Wait until apps are running, and calmed down
4. Create admin user via `make createsuperuser`
5. Manually create site content and config, or use `make seed-for-development` to create basic setup with dummy content (not safe to use if content has already been added)

Once running you should start an interactive shell in `web` container in order to have full access to any Django and Wagtail commands. This can be done via `docker compose exec web bash`, or via our shortcut `make`/`make shell`

We recommend this approach since it makes it a lot easier to tinker and learn how things work. To list all commands available try `python manage.py` (while in the interactive shell)

### 2. Make sure you are ready to commit code

We use pre-commit for making sure all code conforms to the same formatting. This happens automatically on commit after this first time setup.

1. Install [Pre-commit](https://pre-commit.com/#install) (Usually `pip install pre-commit` or `brew install pre-commit`)
2. Activate it via `pre-commit install`

PS. If running code locally instead of in container, poetry installs pre-commit as a dev dependency, so you can run `poetry run pre-commit install` instead.

## Production setup

Site should follow expected Wagtail and Django patterns if nothing else is mentioned.

### Things to keep in mind

- We allow for scheduled content, so make sure to run `publish_scheduled` command every x minutes

## Tests

Use `python manage.py test` in container, or `make test` locally to run test suite. We generally try to rely on Wagtail and Djange framework as much as possible, but feel free to test custom behaviour/code and add sanity checks.

Having test coverage will be helpful when debugging issues or figuring out how existing code was intended to behave (aka. answering the age old question of, is current behaviour a bug or just an unknown feature?).

## Contribute?

This repo is developed and maintained by the [Systemstøtte crew](https://wannabe.gathering.org/tg24/crew#crew-82) at [The Gathering](https://www.gathering.org). Once we get further along PR will be accepted, for now either apply to join our crew or reach out to us via issues before spending any time on development.

## Local development without Docker

It is very possible to run the project locally without Docker. We use poetry for dependency management with poetry-dotenv-plugin to load .env variables. It should automatically make sure python runs in a virtual environment with the correct dependencies, but this method will always require a bit more local management.

### 1. Set up general development and python environment

1. Install `poetry` (we recommend using `pipx` for this, via `pipx install poetry`)
2. Install dependencies by running `poetry install`
3. Install `pre-commit` hooks by running `poetry run pre-commit install`

### 2. Set up and run local postgres database instance

1. Configure and run a local posgres via your method of choice
2. Copy `.env.example` to `.env` and update `POSTGRES_*` variables to match your local setup

### 3. Start development server

1. Run `poetry run python manage.py runserver` to start the development server
2. Run `poetry run python manage.py migrate` to apply migrations
3. Run `poetry run python manage.py createsuperuser` to create a superuser

You can use `poetry env activate` to source poetry env in current shell, if you want to avoid prefixing commands with `poetry run`.
