from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.IntegerField(choices=[
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High')
    ], default=2)  # Example of using choices for priority
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    reminder_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
