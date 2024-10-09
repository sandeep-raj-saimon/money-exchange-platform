from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycurrency.settings')

app = Celery('mycurrency')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover tasks in installed apps
app.autodiscover_tasks()

# Optional: Define a periodic task schedule
app.conf.beat_schedule = {
    'fetch-daily-exchange-rates': {
        'task': 'exchange.tasks.fetch_daily_exchange_rates',
        'schedule': crontab(hour=0, minute=0),  # Runs every day at midnight
    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
