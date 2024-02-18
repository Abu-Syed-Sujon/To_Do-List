' Create your views here.'
# todo/views.py
from django.shortcuts import render, redirect
from .models import Task

def task_list(request):
    tasks = Task.objects.all()
    if request.method == 'POST':
        if 'clear_all' in request.POST:
            Task.objects.all().delete()
        elif 'save_all' in request.POST:
            # Implement save all logic if needed
            pass
        elif 'mark_all_done' in request.POST:
            Task.objects.all().update(completed=True)
        return redirect('task_list')
    return render(request, 'todo/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        Task.objects.create(title=title)
        return redirect('task_list')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')
