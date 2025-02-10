# Defining environment
ARG APP_ENV=dev

# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
# Supported python3 versions: https://docs.wagtail.org/en/stable/releases/upgrading.html#compatible-django-python-versions
FROM python:3.13-slim-bookworm AS base

# Remember to also update in pyproject.toml and GitHub Workflows
ENV POETRY_VERSION=2.0.1

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set default environment variables.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Install poetry
RUN pip install poetry==${POETRY_VERSION}

# Main building step, only used for production since on dev we want things to be less static
FROM base AS production-builder
RUN echo "Generating production environment"
WORKDIR /app

# Install production/main dependencies into .venv (in-project) directory
COPY poetry.lock pyproject.toml ./
RUN poetry config virtualenvs.in-project true \
	&& poetry install --only main --no-interaction --no-ansi

# Create final production image by copying the built virtual environment and the source code
FROM base AS production-image
#FROM python:3.13-slim-bookworm AS production-image
RUN echo "Constructing final production image"
WORKDIR /app

# Prepare final application folder and environment
ENV DJANGO_SETTINGS_MODULE=tgno.settings.production
ENV PATH="/app/.venv/bin:$PATH"
COPY --from=production-builder /app/.venv /app/.venv
COPY . .
RUN python manage.py collectstatic --noinput --clear

ENTRYPOINT ["/app/entrypoint.prod.sh"]
CMD ["gunicorn", "tgno.wsgi:application"]

# Create final production image for hosting static files (when desired)
FROM nginx:1.27-alpine AS nginx-production-image
RUN echo "Building nginx-production image for static file hosting"
COPY --from=production-image /app/static /usr/share/nginx/html/static

# Create final development image, which assumes that the source code is mounted as a volume
FROM base AS dev-image
RUN echo "Preparing final development image"
WORKDIR /app
ENV DJANGO_SETTINGS_MODULE=tgno.settings.dev
ENTRYPOINT ["/app/entrypoint.dev.sh"]

FROM ${APP_ENV}-image
