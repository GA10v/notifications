python admin_panel/src/manage.py collectstatic --noinput
python admin_panel/src/manage.py migrate
python admin_panel/src/manage.py createsuperuser --noinput || true
gunicorn --chdir ./admin_panel/src config.wsgi:application -b :8000
