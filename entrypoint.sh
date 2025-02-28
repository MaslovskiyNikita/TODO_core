#!/bin/sh

poetry run python app/api/v1/manage.py makemigrations projects
poetry run python app/api/v1/manage.py migrate


exec poetry run python app/api/v1/manage.py runserver 0.0.0.0:8000