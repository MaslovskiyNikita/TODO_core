#!/bin/sh

poetry run python application/manage.py makemigrations
poetry run python application/manage.py migrate

poetry run python application/manage.py runserver 0.0.0.0:8000 
