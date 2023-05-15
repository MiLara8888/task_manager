from django import template
from shed.models import User, Project, Task, Comment

register = template.Library()

@register.simple_tag()
def count_inwork(project_pk=None, user_id=None):
    """определения количества задач в работе для каждого пользователя в каждом отдельном проекте"""
    return len(Task.objects.filter(project=project_pk, state='IWO'))