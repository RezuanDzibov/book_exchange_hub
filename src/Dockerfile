FROM python:3.11-slim

RUN apt update \
    && apt install python3 netcat curl -y \
    && rm -rf /var/cache/apt/* /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    \
    # python
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_VERSION=1.4.2\
    \
    APP_HOME="/home/app" \
    PATH="/opt/poetry/bin:$PATH" \
    PATH="/root/.local/bin:$PATH"

WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock $APP_HOME

RUN pip install --upgrade pip \
  && curl -sSL https://install.python-poetry.org | python \
  && poetry config virtualenvs.create false \
  && poetry install --only main --no-interaction --no-ansi --no-root

COPY . $APP_HOME

RUN chmod +x $APP_HOME/entrypoint.sh
ENTRYPOINT ["/home/app/entrypoint.sh"]