import os
from celery import Celery
from django.apps import AppConfig

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mytodo.settings')

app = Celery('mytodo')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
