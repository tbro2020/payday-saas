#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# run a worker :)
celery -A payday worker -l info -c 4 --beat -E