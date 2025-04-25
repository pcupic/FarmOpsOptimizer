from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from .forms import TaskForm
from django.contrib.auth.decorators import login_required

def task_list(request):
    tasks = Task.objects.all().filter(user=request.user)  
    
    title = request.GET.get('title', '')
    if title:
        tasks = tasks.filter(title__icontains=title)  
    
    priority = request.GET.get('priority', '').upper()
    if priority:
        if priority in dict(Task.PRIORITY_CHOICES):
            tasks = tasks.filter(priority=priority)
    
    start_date = request.GET.get('start_date', '')
    if start_date:
        tasks = tasks.filter(start_date__gte=start_date)
    
    due_date = request.GET.get('due_date', '')
    if due_date:
        tasks = tasks.filter(due_date__lte=due_date)
    
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user  
            task.save() 
            return redirect('task_list')  
    else:
        form = TaskForm()

    return render(request, 'create_task.html', {'form': form})

@login_required
def edit_task(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'edit_task.html', {'form': form, 'task': task})

@login_required
def delete_task(request, id):
    task = get_object_or_404(Task, id=id)  
    if request.method == 'POST':
        task.delete()  
        return redirect('task_list')  
    
