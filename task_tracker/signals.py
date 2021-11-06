from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Task, StatusChange
from .tasks import send_email_message


@receiver(pre_save, sender=Task)
def updated_task_status(sender, instance: Task, **kwargs):
    if instance.id:
        previous = Task.objects.get(id=instance.id)
        if previous.status != instance.status:
            # Асинхронная отправка сообщения
            send_email_message.delay(instance.id)
            StatusChange.objects.create(
                previous_status=previous.status,
                next_status=instance.status,
                task=instance, user=instance.performer)
