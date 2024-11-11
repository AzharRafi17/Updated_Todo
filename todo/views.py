from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User  
from .models import Category, Task
from .forms import TaskForm
from django.contrib import messages
from .tasks import send_reminder_email
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

def home(request):
    return render(request, 'home.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect('login')
        
        login(request, user)
        return redirect('task_list')
    
    return render(request, 'login.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken")
            return redirect('register')
        
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        
        messages.success(request, "Account created successfully")
        return redirect('login')

    return render(request, 'register.html')

@login_required(login_url='login')
def task_list(request):
    user_tasks = Task.objects.filter(user=request.user)
    
    # Filter by completion status
    filter_by = request.GET.get('filter', 'all')
    if filter_by == 'completed':
        user_tasks = user_tasks.filter(completed=True)
    elif filter_by == 'incomplete':
        user_tasks = user_tasks.filter(completed=False)

    # Sorting tasks
    sort_by = request.GET.get('sort', 'due_date')
    if sort_by == 'priority':
        user_tasks = user_tasks.order_by('-priority')
    else:
        user_tasks = user_tasks.order_by('due_date')
        
    upcoming_tasks = Task.objects.filter(
        user=request.user,
        reminder_time__lte=timezone.now() + timedelta(minutes=1),
        reminder_time__gt=timezone.now(),
        completed=False 
    )

    for task in upcoming_tasks:
        
        send_reminder_email.apply_async((task.id,), eta=task.reminder_time)

    return render(request, 'index.html', {'user_task': user_tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        reminder_time = request.POST.get('reminder_time')
        priority = request.POST.get('priority')

        category_name = request.POST.get('category')

        
        category = Category.objects.filter(name=category_name).first()

        if category and title and due_date:
            task = Task.objects.create(
                user=request.user,
                title=title,
                description=description,
                due_date=due_date,
                reminder_time=reminder_time,
                priority=priority,
                category=category
            )
            task.save()

   
    user_tasks = Task.objects.filter(user=request.user)
    
    # Filter by completion status
    filter_by = request.GET.get('filter', 'all')
    if filter_by == 'completed':
        user_tasks = user_tasks.filter(completed=True)
    elif filter_by == 'incomplete':
        user_tasks = user_tasks.filter(completed=False)

    # Sorting tasks
    sort_by = request.GET.get('sort', 'due_date')
    if sort_by == 'priority':
        user_tasks = user_tasks.order_by('-priority')
    else:
        user_tasks = user_tasks.order_by('due_date')

    return render(request, 'index.html', {'user_task': user_tasks})

@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)

            # Manually update the category if needed
            category_name = request.POST.get('category')
            category = Category.objects.filter(name=category_name).first()
            if category:
                task.category = category
            

            task.save()

            # Check if reminder time is set and send reminder email
            if task.reminder_time:
                send_reminder_email.apply_async((task.id,), eta=task.reminder_time)
            
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit.html', {'form': form, 'task': task})


@login_required(login_url='login')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)  
    task.delete()
    return redirect('task_list')

@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user) 
    task.completed = not task.completed
    task.save()
    return redirect('task_list')

def logout_user(request):
    logout(request)
    return redirect('home') 