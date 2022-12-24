#!/usr/bin/env sh

set -e

wait-for-it.sh \
    -h "$SIMPLE_SALES_BACKEND_DOCKER_ENTRYPOINT_DB_HOST" \
    -p "$SIMPLE_SALES_BACKEND_DOCKER_ENTRYPOINT_DB_PORT"

# 'VENV_PATH' is set in the Dockerfile
"$VENV_PATH"/bin/python -m simple_sales "$@"
