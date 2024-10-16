# Defining environment
ARG APP_ENV=dev

# Use an official Python runtime based on Debian 12 "bookworm" as a parent image.
# Supported python3 versions: https://docs.wagtail.org/en/stable/releases/upgrading.html#compatible-django-python-versions
FROM python:3.12-slim-bookworm AS base

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set default environment variables.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000

# Install system packages required by Wagtail and Django.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    netcat-openbsd \
 && rm -rf /var/lib/apt/lists/*

# Install the application server.
RUN pip install "gunicorn==23.0.0"

# Install the project requirements.
COPY requirements.txt /
RUN pip install -r /requirements.txt

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Building the Production image
FROM base AS production-image
RUN echo "Building production image"
ENV DJANGO_SETTINGS_MODULE=tgno.settings.production
RUN python manage.py collectstatic --noinput --clear
ENTRYPOINT ["/app/entrypoint.prod.sh"]
CMD ["gunicorn", "tgno.wsgi:application"]

# Building the nginx production image
FROM nginx:1.27-alpine AS nginx-production-image
RUN echo "Building nginx-production image"
COPY --from=production-image /app/static /usr/share/nginx/html/static

# Building the Dev image
FROM base AS dev-image
RUN echo "Building dev image"
ENV DJANGO_SETTINGS_MODULE=tgno.settings.dev
RUN python manage.py collectstatic --noinput --clear
CMD ["python", "manage.py", "0.0.0.0:8000"]

FROM ${APP_ENV}-image