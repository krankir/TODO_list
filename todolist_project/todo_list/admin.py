from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Task, Work


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_date', 'user', )


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'completed', 'due_date', 'task', )
