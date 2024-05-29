#!/bin/sh

# Wait for the server volume to be available
until cd /app/backend
do
    echo "Waiting for server volume..."
done

# Wait for the database to be ready and apply migrations
until python manage.py makemigrations
do
    echo "Waiting for db to be ready..."
    sleep 2
done

until python manage.py migrate
do
    echo "Waiting for db to be ready..."
    sleep 2
done

# Uncomment if you need to create a superuser automatically
# until python manage.py createsuperuser --noinput --email info@sycamore.cd
# do
#     echo "Waiting for superuser to be created..."
# done

# Uncomment to collect static files (usually needed for production)
# python manage.py collectstatic --noinput

# Start the Gunicorn server
exec gunicorn payday.wsgi:application --bind 0.0.0.0:8000
