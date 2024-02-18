'todo/urls.py'
from django.urls import path
from .views import task_list, add_task, complete_task

urlpatterns = [
    path('', task_list, name='task_list'),
    path('add/', add_task, name='add_task'),
    path('complete/<int:task_id>/', complete_task, name='complete_task'),
]
