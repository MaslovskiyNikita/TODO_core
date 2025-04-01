#!/bin/sh

poetry run python application/manage.py makemigrations
poetry run python application/manage.py migrate

poetry run python application/manage.py runserver 0.0.0.0:8000 

apt-get update && apt-get install -y telnet
telnet smtp.gmail.com 587