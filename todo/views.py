from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm


@login_required
def task_list(request):
    """ its show all task  """
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')  # pylint: disable=no-member
    form = TaskForm()
    context = {
        'tasks': tasks,
        'form': form
    }
    return render(request, 'todo/task_list.html', context)


@login_required
def add_task(request):
    """Add a new task for the authenticated user."""
    if request.method == 'POST':
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

    return redirect('task_list')

@login_required
def delete_task(request, task_id):
    """Delete a task for the authenticated user."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todo/delete_task.html', {'task': task})

@login_required
def update_task(request, task_id):
    """Update a task for the authenticated user."""
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form= TaskForm(request.POST, instance=task)  # Re-populate form with submitted data and errors
    return render(request, 'todo/update_task.html', {'form': form})

@login_required
def complete_task(request, task_id):
    """Mark a task as complete/incomplete for the authenticated user."""
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id, user=request.user)

        task.completed = not task.completed
        task.save()

    return redirect('task_list')


@login_required
def task_bulk_action(request):
    """Perform bulk actions on tasks for the authenticated user."""
    if request.method == 'POST':
        action = request.POST.get('action')

        tasks = Task.objects.filter(user=request.user)  # pylint: disable=no-member

        if action == 'clear_all':
            tasks.delete()

        elif action == 'mark_all_done':
            tasks.update(completed=True)

    return redirect('task_list')
