#!/bin/sh

# Wait for the server volume to be available
until cd /app/backend
do
    echo "Waiting for server volume..."
done

# Start the Celery worker with beat
exec celery -A payday worker -l info -c 4 --beat -E
