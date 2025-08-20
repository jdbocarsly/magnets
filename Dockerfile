ARG UV_VERSION="0.8.4"
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_image

FROM python:3.10 AS api
SHELL ["/bin/bash", "--login", "-c"]

COPY --from=uv_image /uv /usr/local/bin/uv
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/.venv \
    UV_PYTHON=python3.10

WORKDIR /app

WORKDIR /app

COPY . .
RUN uv sync --locked --no-dev --all-extras

# This will define the number of gunicorn workers
ARG WEB_CONCURRENCY=1
ENV WEB_CONCURRENCY=${WEB_CONCURRENCY}

ARG PORT=5001
EXPOSE ${PORT}
ENV PORT=${PORT}

CMD ["/bin/bash", "-c", "/opt/.venv/bin/python -m gunicorn --preload -w ${WEB_CONCURRENCY} 'magnet_main:app'"]
