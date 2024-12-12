from celery.schedules import crontab
from celery import Celery
import os, ssl

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payday.settings')

# Define a more descriptive variable name for `REDIS_URL`.
REDIS_URL_WITH_SSL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

# Define more descriptive variable names for `broker_use_ssl` and `redis_backend_use_ssl`.
REDIS_BACKEND_USE_SSL_CONFIG = {'ssl_cert_reqs': ssl.CERT_NONE}
BROKER_USE_SSL_CONFIG = {'ssl_cert_reqs': ssl.CERT_NONE}


# Define a function to check if the REDIS_URL starts with `rediss://`.
def is_redis_url_with_ssl(redis_url):
    return redis_url.startswith('rediss://')

# Create the Celery app.
app = Celery("payday")

# Check if the REDIS_URL starts with `rediss://`. If it does, set the `broker_use_ssl`
# and `redis_backend_use_ssl` variables accordingly.
if is_redis_url_with_ssl(REDIS_URL_WITH_SSL):
    app = Celery("payday", broker_use_ssl=BROKER_USE_SSL_CONFIG,
                 redis_backend_use_ssl=REDIS_BACKEND_USE_SSL_CONFIG,
                 broker_connection_retry_on_startup=True)

# Configure the Celery app from the Django settings and autodiscover the tasks.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'hourly': {
        'task': 'hourly',  
        'schedule': crontab(minute=0)
    },
    'daily': {
        'task': 'daily',  
        'schedule': crontab(minute=0, hour=23)
    },
    'weekly': {
        'task': 'weekly',  
        'schedule': crontab(minute=0, hour=23, day_of_week=0)
    },
    'monthly': {
        'task': 'monthly',  
        'schedule': crontab(minute=0, hour=23, day_of_month=1)
    },
    'yearly': {
        'task': 'yearly',  
        'schedule': crontab(minute=0, hour=23, day_of_month=1, month_of_year=1)
    }
}

if __name__ == '__main__':
    app.start()