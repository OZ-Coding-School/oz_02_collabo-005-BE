#!/bin/sh
set -e
python manage.py wait_for_db
python manage.py migrate
uwsgi --ini "/okivery/app/uwsgi/uwsgi.ini"
