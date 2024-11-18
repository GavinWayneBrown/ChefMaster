from django import template
from datetime import timedelta

register = template.Library()

@register.filter
def human_readable_duration(value):
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"{hours}hr, {minutes}min"
    return value     