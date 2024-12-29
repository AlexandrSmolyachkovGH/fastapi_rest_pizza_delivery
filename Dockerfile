FROM python:3.10

WORKDIR /pizza_app

ENV PYTHONPATH=/pizza_app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./pyproject.toml ./poetry.lock ./

RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client libpq-dev build-essential curl netcat-openbsd && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

RUN pip install bcrypt==3.2.0

COPY . .



