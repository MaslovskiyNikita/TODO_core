#!/bin/sh

poetry run python application/manage.py makemigrations projects
poetry run python application/manage.py migrate


exec poetry run python application/manage.py runserver 0.0.0.0:8000