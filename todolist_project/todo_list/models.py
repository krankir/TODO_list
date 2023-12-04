from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    """Таблица для задач."""

    title = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Work(models.Model):
    """Таблица рабочих процессов."""

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
