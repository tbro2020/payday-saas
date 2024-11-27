#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

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

#until python manage.py createsuperuser --noinput --email info@sycamore.cd
#do
#    echo "Waiting for superuser to be created ..."
#done

# python manage.py collectstatic --noinput
# gunicorn payday.wsgi:application --bind 0.0.0.0:8000 --autoscale=4,1

gunicorn payday.wsgi --bind 0.0.0.0:8080 --workers 4 --threads 4