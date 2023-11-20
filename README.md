# TG.no - Backend

**NB** Public repo. So avoid pushing secrets...

CMS and REST API built using [Wagtail](https://wagtail.org/). It runs on [http://localhost:8000](http://localhost:8000) by default. With admin pages exposed on [http://localhost:8000/admin](http://localhost:8000/admin) and API exposed at [http://localhost:8000/api/v2/](http://localhost:8000/api/v2/)

For actual production usage we will most likely rely entierly on [REST API](https://docs.wagtail.org/en/stable/advanced_topics/api/v2/configuration.html), so consider all templates and html views test/dev only.

Initial site following structure as outlined in official [Getting Started tutorial](https://docs.wagtail.org/en/stable/getting_started/tutorial.html). So check that out for a quick introduction into how contents are structured.

## Current state

- Following Wagtail getting started tutorial
- `aktuelt` app is combination of `blog` from tutorial and start of actual Aktuelt section
- REST API requirements in place and certain routes exposed via `api.py` files (mapped in `tgno/urls.py`)
- `home` and `search` apps are init/tutorial leftovers

Example urls
- [Aktuelt / News API](http://localhost:8000/api/v2/news/)
- [Aktuelt section / news page](http://localhost:8000/aktuelt/)

**Prioritized tasks:**

- [x] Get local `docker-compose` based development setup functional and documented
- [.] Get local editor tooling functional and documented
- [ ] Get staging environment up and running using terraform (in another repo for now)
- [ ] Limit sub-page types available on `aktuelt` app
- [ ] Start iterating on `aktuelt` app to get a minimal realistic and functional article setup in place  (look at existing page for inspiration)
- [ ] Iterate on README and other docs to include any relevant commands and setup steps

## Getting started

### 1. Get things up and running locally

We are using Docker via docker-compose for local development. To get started

1. Copy `.env.example` to `.env`
2. Start apps via `docker-compose up`
3. Wait until apps are running, and calmed down
4. Create admin user via `make createsuperuser`

Once running you should start an interactive shell in `web` container in order to have full access to any Django and Wagtail commands. This can be done via `docker-compose exec web bash`, or via our shortcut `make`/`make shell`

We recommend using the for most commands as there is no value in duplicating all simple commands in local make files, and it makes i a lot easier to tinker and learn how things work. To list all commands available try `python manage.py` (while in the interactive shell)

## Contribute?

This repo is developed and maintained by the [Systemstøtte crew](https://wannabe.gathering.org/tg24/crew#crew-82) at [The Gathering](https://www.gathering.org). Once we get further along PR will be accepted, for now either apply to join our crew or reach out to us via issues before spending any time on development.
