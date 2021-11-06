from django.utils import timezone
from django import template

register = template.Library()


# Задача просрочена
@register.simple_tag
def is_expired(date_time):
    if date_time:
        today = timezone.now()
        if date_time < today:
            return True
    return False
