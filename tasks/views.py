from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q

from .forms import SignUpForm, LoginForm, TaskForm, CategoryForm
from .models import Task, Category

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'tasks/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'tasks/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    # Get tasks status counts
    tasks_total = Task.objects.filter(user=request.user).count()
    tasks_completed = Task.objects.filter(user=request.user, completed=True).count()
    tasks_pending = tasks_total - tasks_completed
    
    # Get tasks with upcoming due dates
    upcoming_tasks = Task.objects.filter(
        user=request.user, 
        completed=False, 
        due_date__isnull=False, 
        due_date__gt=timezone.now()
    ).order_by('due_date')[:5]
    
    # Get tasks by priority
    high_priority = Task.objects.filter(user=request.user, priority='high', completed=False).count()
    medium_priority = Task.objects.filter(user=request.user, priority='medium', completed=False).count()
    low_priority = Task.objects.filter(user=request.user, priority='low', completed=False).count()
    
    # Get tasks by category
    categories = Category.objects.filter(user=request.user).annotate(task_count=Count('tasks'))
    
    context = {
        'tasks_total': tasks_total,
        'tasks_completed': tasks_completed,
        'tasks_pending': tasks_pending,
        'upcoming_tasks': upcoming_tasks,
        'high_priority': high_priority,
        'medium_priority': medium_priority,
        'low_priority': low_priority,
        'categories': categories,
    }
    
    return render(request, 'tasks/dashboard.html', context)

@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    filter_status = request.GET.get('status', '')
    filter_priority = request.GET.get('priority', '')
    filter_category = request.GET.get('category', '')
    
    tasks = Task.objects.filter(user=request.user)
    
    if search_query:
        tasks = tasks.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))
    
    if filter_status == 'completed':
        tasks = tasks.filter(completed=True)
    elif filter_status == 'pending':
        tasks = tasks.filter(completed=False)
    
    if filter_priority:
        tasks = tasks.filter(priority=filter_priority)
    
    if filter_category:
        tasks = tasks.filter(category__id=filter_category)
    
    categories = Category.objects.filter(user=request.user)
    
    context = {
        'tasks': tasks,
        'categories': categories,
        'search_query': search_query,
        'filter_status': filter_status,
        'filter_priority': filter_priority,
        'filter_category': filter_category,
    }
    
    return render(request, 'tasks/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(request.user)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Create Task'})

@login_required
def task_edit(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = TaskForm(request.user, request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(request.user, instance=task)
    
    return render(request, 'tasks/task_form.html', {'form': form, 'title': 'Edit Task'})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

@login_required
def task_toggle_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    
    return redirect('task_list')

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user).annotate(task_count=Count('tasks'))
    return render(request, 'tasks/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'tasks/category_form.html', {'form': form, 'title': 'Create Category'})

@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'tasks/category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category deleted successfully!')
        return redirect('category_list')
    
    return render(request, 'tasks/category_confirm_delete.html', {'category': category})