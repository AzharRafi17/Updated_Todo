import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytodo.settings')

app = Celery('mytodo')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
TIME_ZONE = 'Asia/Karachi' 
USE_TZ = True 

app.conf.beat_schedule = {
    'send-reminder-email-every-minute': {
        'task': 'todo.tasks.send_reminder_email',
        'schedule': crontab(minute='*/1'),  # Runs every minute
    },
}
