# from django import forms
# from .models import Task

# class TaskForm(forms.ModelForm):
#     class Meta:
#         model = Task 
#         fields = ['title', 'description', 'due_date', 'priority', 'category', 'reminder_time']
#         widgets = {
#             'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#             'reminder_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
#         }
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'reminder_time', 'priority', 'category']
