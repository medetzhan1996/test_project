from django.contrib import admin
from .models import Task, TaskChekList, StatusChange, Reminder

admin.site.register(Task)
admin.site.register(TaskChekList)
admin.site.register(StatusChange)
admin.site.register(Reminder)
