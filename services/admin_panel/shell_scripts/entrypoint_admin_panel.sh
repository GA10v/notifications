#!/bin/sh
python3 manage.py migrate
python3 manage.py createsuperuser --noinput
python3 manage.py collectstatic --noinput
python3 manage.py compilemessages
uwsgi --strict --ini uwsgi/uwsgi.ini
cd src && gunicorn --bind 0.0.0.0:8080 -w 4 -k uvicorn.workers.UvicornH11Worker main:app