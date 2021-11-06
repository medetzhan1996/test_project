from celery import shared_task
from django.core.mail import send_mail
from .models import Task


# Чтобы использовать Celery установите на сервер RabbitMQ
@shared_task
def send_email_message(task_id):
    task = Task.objects.get(id=task_id)
    emails = list(task.observers.values_list('email', flat=True))
    message = f"Изменен статус  задачи {task.title} на {task.status}"
    mail_sent = send_mail(
        'Изменен статус задачи',
        message,
        'medet@gmail.com',
        emails,
        fail_silently=False,
    )
    return mail_sent
