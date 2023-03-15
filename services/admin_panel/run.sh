#!/bin/sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser --noinput \
                                --username $DJANGO_SUPERUSER_USERNAME \
                                --email $DJANGO_SUPERUSER_EMAIL
python3 manage.py collectstatic --noinput
python3 manage.py compilemessages
uwsgi --strict --ini uwsgi/uwsgi.ini