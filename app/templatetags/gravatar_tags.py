from django import template
from app.utils import get_gravatar_url

register = template.Library()

@register.filter
def gravatar_url(email, size=40):
    return get_gravatar_url(email, size)
