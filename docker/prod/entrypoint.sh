#!/bin/sh
set -e

while ! pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

uwsgi --ini /uwsgi.ini

exec "$@"
