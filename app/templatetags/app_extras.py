from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Pobiera element ze słownika po kluczu"""
    return dictionary.get(key)

@register.filter
def has_voted(game, user):
    """Sprawdza czy użytkownik zagłosował już na daną grę"""
    return game.vote_set.filter(user=user).exists()

@register.filter
def sub(value, arg):
    """Odejmuje arg od value"""
    return value - arg
