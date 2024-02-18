'Create your models here'
from django.db import models
from django.db.models import Manager


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    objects: Manager['Task']
    def __str__(self):
        return "Task"
