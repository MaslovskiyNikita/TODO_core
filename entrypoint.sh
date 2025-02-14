#!/bin/sh

echo "POSTGRES_DB: $POSTGRES_DB"
echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_PASSWORD: $POSTGRES_PASSWORD"
echo "HOST: $HOST"
echo "PORT: $PORT"

poetry run python app/manage.py makemigrations core

poetry run python app/manage.py migrate

exec poetry run python app/manage.py runserver 0.0.0.0:8000