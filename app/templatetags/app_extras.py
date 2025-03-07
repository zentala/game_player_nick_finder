from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Pobiera element ze słownika po kluczu"""
    return dictionary.get(key)
