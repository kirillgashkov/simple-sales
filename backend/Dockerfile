FROM python:3.11-slim-bullseye

WORKDIR /app/


# Install Poetry

ENV POETRY_HOME=/opt/poetry \
    POETRY_VERSION=1.2.2

RUN python -m venv "$POETRY_HOME" \
 && "$POETRY_HOME/bin/pip" install poetry=="$POETRY_VERSION"


# Install non-Python dependencies

ENV MIGRATE_RELEASE_TAG=v4.15.2
ENV WAIT_FOR_IT_COMMIT=81b1373f17855a4dc21156cfe1694c31d7d1792e

RUN apt-get update \
 && apt-get install -y \
                       curl \
                       # 'gcc' and 'libpq-dev' are used to build 'psycopg2'
                       # Python package.
                       gcc \
                       libpq-dev \
 && curl -sSL https://github.com/golang-migrate/migrate/releases/download/${MIGRATE_RELEASE_TAG}/migrate.linux-amd64.tar.gz | tar -xz -C /usr/local/bin migrate \
 && curl -sSL https://raw.githubusercontent.com/vishnubob/wait-for-it/${WAIT_FOR_IT_COMMIT}/wait-for-it.sh > /usr/local/bin/wait-for-it.sh && chmod +x /usr/local/bin/wait-for-it.sh


# Install Python dependencies

ENV VENV_PATH="/venv"

COPY poetry.lock pyproject.toml /app/

RUN python -m venv "$VENV_PATH" \
 && . "$VENV_PATH/bin/activate" \
 && "$POETRY_HOME/bin/poetry" install --no-root --no-interaction --no-ansi


# Copy sources

COPY ./ /app/


ENTRYPOINT ["/app/docker-entrypoint.sh"]
