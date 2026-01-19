#!/bin/sh
set -e

mkdir -p media/cron_logs
touch media/cron_logs/cron.log

python manage.py makemigrations
python manage.py migrate
if [ "$DJANGO_SUPERUSER_USERNAME" ]; then
    python manage.py createsuperuser \
        --no-input \
        --username "$DJANGO_SUPERUSER_USERNAME" \
        --email "$DJANGO_SUPERUSER_EMAIL" || true
fi

exec "$@"