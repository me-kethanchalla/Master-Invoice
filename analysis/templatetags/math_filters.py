from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return float(value) / float(arg) if float(arg) != 0 else 'NaN'
    except (ValueError, TypeError):
        return 'NaN'