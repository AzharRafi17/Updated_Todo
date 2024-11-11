from celery import shared_task
from django.core.mail import send_mail
from .models import Task
from django.utils import timezone
from datetime import timedelta

@shared_task

def send_reminder_email():
    try:
        tasks = Task.objects.filter(
        reminder_time__exact=timezone.now(),
        reminder_time__isnull=False
)

        
        # Loop through all tasks and send email reminders
        for task in tasks:
            # print(task.reminder_time)
            print(task.reminder_time)
            send_mail(
                subject=f'Reminder: {task.title}',
                message=f'You have a task "{task.title}" due at {task.due_date}. Please complete it on time.',
                from_email='muhammadazharali17@gmail.com', 
                recipient_list=[task.user.email],
                fail_silently=False,
            )
    except Task.DoesNotExist:
        pass
