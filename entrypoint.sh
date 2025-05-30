#!/bin/bash

python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py collectstatic --no-input --clear
python manage.py createsuperuser --noinput --username atid --email admin@dev.com
exec daphne -p 8000 -b 0.0.0.0 CTFBackend2025.asgi:application
