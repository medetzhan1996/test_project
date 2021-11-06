from django.db import models
from django.conf import settings

STATUS_CHOICES = (
    (0, "Планируется"),
    (1, "Активная"),
    (2, "Контроль"),
    (3, "Завершена")
)


# Базовый абстрактный класс
class ItemBase(models.Model):
    title = models.CharField(max_length=180)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title


# Задача
class Task(ItemBase):
    description = models.TextField()
    performer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='performer_tasks')
    observers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='observers_tasks')
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)
    planned_end_datetime = models.DateTimeField()


# Чек лист задачи
class TaskChekList(ItemBase):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)


# Изменение статуса
class StatusChange(models.Model):
    previous_status = models.IntegerField(choices=STATUS_CHOICES)
    next_status = models.IntegerField(choices=STATUS_CHOICES)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


# Напоминание
class Reminder(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    description = models.TextField()
    users = models.ManyToManyField(settings.AUTH_USER_MODEL)
