web: gunicorn --bind 0.0.0.0:8000 payday.wsgi:application
worker: celery -A payday worker -l INFO -E