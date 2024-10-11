from celery import shared_task
from django.utils import timezone
from .models import Task

@shared_task
def check_reminders():
    tasks = Task.objects.filter(reminder_time__lte=timezone.now())
    for task in tasks:
        print(f"Reminder: {task.title} is due!")