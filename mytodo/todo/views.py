from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Task, Category
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .tasks import check_reminders
    
@login_required(login_url='login')
def todoList(request):
    # returns the tasks of the current user
    todos = Task.objects.filter(user=request.user)
    
    selected_category = request.GET.get('category')
    
    if selected_category:
        todos = todos.filter(category__name=selected_category)
    
    sort_by = request.GET.get('sort_by')
    
    if sort_by == 'due_date_desc':
        todos = todos.order_by('-due_date')
    elif sort_by == 'due_date_asc':
        todos = todos.order_by('due_date')
    elif sort_by == 'priority_asc':
        todos = todos.order_by('priority')
    elif sort_by == 'priority_desc':
        todos = todos.order_by('-priority')

    return render(request, 'index.html', {'todos': todos})
    
@login_required(login_url='login')
def create_todo(request):
    if request.method == 'POST':
        desciption = request.POST.get('description')
        title = request.POST.get('title')
        priority = request.POST.get('priority') or 1
        duedate = request.POST.get('duedate')
        category = request.POST.get('category')
        category = Category.objects.create(name=category)
        reminder_time = request.POST.get('reminder_time')
        # Task.objects.create(user=request.user, title=title, desciption=desciption, priority=priority, due_date=duedate, category=category,reminder_time=reminder_time)
        task = Task( 
            title=title,
            desciption=desciption,
            due_date=duedate,
            reminder_time=reminder_time,
            category=category,
            priority=priority,
            user=request.user
        )  
        task.save()  
    return redirect('todo_list')
    

@login_required(login_url='login')
def complete_todo(request, todo_id):
    todo = Task.objects.get(id=todo_id, user=request.user)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

@login_required(login_url='login')
def delete_todo(request, todo_id):
    todo = Task.objects.get(id=todo_id, user=request.user)
    todo.delete()
    return redirect('todo_list')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"Invalid username or password")
            return redirect('login')
        
        user = authenticate(username = username, password= password) # verifies and returns a User Object with credentials

        if user is None:    # Checks again for the returned User Object
            messages.error(request,"Invalid Credentials")
            return redirect('login')
        
        else:   # if the returned credential are valid it logs in the user
            login(request, user)
            return redirect('todo_list')
    
    
    return render(request,'login.html')
    
def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = User.objects.filter(username = username)
        
        if user.exists():
            messages.info(request, "User already taken")
            return redirect('register')
        
        user = User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        
        messages.info(request,"Account created successfully")
        
        return redirect('register')
    return render (request,'register.html')

def logout_page(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def edit_task(request, todo_id):
    
    task = Task.objects.get(id=todo_id)
    
    if request.method == 'POST':
        task.desciption = request.POST.get('description')
        task.title = request.POST.get('title')
        task.priority = request.POST.get('priority') or 1
        task.due_date = request.POST.get('duedate')
        reminder_time = request.POST.get('reminder_time')
        category_name = request.POST.get('category')
        categories = Category.objects.filter(name=category_name)
        
        if categories.exists():
            category = categories.first()  # Get the first category found
        else:
        # Optionally create the category if it doesn't exist
            category = Category.objects.create(name=category_name)

        task.category = category
        task.save()
        return redirect('todo_list')
    
    return render(request, 'edit.html', {'task':task})

def create_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        desciption= request.POST('desciption')
        due_date = request.POST['due_date']
        task.priority = request.POST.get('priority') or 1
        reminder_time = request.POST.get['reminder_time']  # Capture reminder time
        task = Task.objects.create(
            title=title,
            desciption=desciption,
            due_date=due_date,
            reminder_time=reminder_time,
            user=request.user
        )
        task.save()
        check_reminders.delay()  # This will run the check_reminders task asynchronously
        

        return render(request, 'create_task.html')  
        return redirect('task_list')  # Redirect to task list view

    return render(request, 'tasks.html')