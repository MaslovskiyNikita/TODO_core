#!/bin/sh

poetry run python app/manage.py makemigrations projects
poetry run python app/manage.py makemigrations tasks

poetry run python app/manage.py migrate


exec poetry run python app/manage.py runserver 0.0.0.0:8000