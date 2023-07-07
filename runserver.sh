#!/bin/sh

. .venv/bin/activate
python -Wa manage.py runserver 0:8080
