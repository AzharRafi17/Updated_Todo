from celery import shared_task
from django.core.mail import send_mail
from .models import Task
from datetime import timedelta

@shared_task
def send_reminder_email(task_id):
    print("RUNNING TASK")
    task = Task.objects.get(id=task_id)
    print(task.user.email)
    send_mail(
        subject=f'Reminder: {task.title}',
        message=f'You have a task "{task.title}" due at {task.due_date}. Please complete it on time.',
        from_email='muhammadazharali17@gmail.com', 
        recipient_list=[task.user.username],
        fail_silently=False
    )
