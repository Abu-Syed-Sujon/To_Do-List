from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    form = TaskForm()

    return render(request, 'todo/task_list.html', {
        'tasks': tasks,
        'form': form
    })


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

    return redirect('task_list')


@login_required
def complete_task(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)

        task.completed = not task.completed
        task.save()

    return redirect('task_list')


@login_required
def task_bulk_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')

        tasks = Task.objects.filter(user=request.user)

        if action == 'clear_all':
            tasks.delete()

        elif action == 'mark_all_done':
            tasks.update(completed=True)

    return redirect('task_list')
