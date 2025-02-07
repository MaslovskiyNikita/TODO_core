#!/bin/sh

# Запускаем миграции
poetry run python app/manage.py migrate

# Запускаем сервер
exec poetry run python app/manage.py runserver 0.0.0.0:8000