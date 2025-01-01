from django import template

register = template.Library()

@register.filter
def notification_alert_icon(tag):
    # Icon class based on the tag
    return {
        'success': 'bi-check-circle-fill',
        'info': 'bi-info-circle-fill',
        'warning': 'bi-exclamation-triangle-fill',
        'error': 'bi-exclamation-triangle-fill',
        'debug': 'bi-bug-fill',
    }.get(tag, 'bi-info-circle-fill')  # Default to info icon

@register.filter
def notification_alert_color(tag):
    # Alert class based on the tag
    return {
        'success': 'success',
        'info': 'primary',
        'warning': 'warning',
        'error': 'danger',
        'debug': 'white',
    }.get(tag, 'danger')  # Default to primary
