from django import template

register = template.Library()

@register.filter
def dict_key(d, key):
    """Retrieve a value from a dictionary by key."""
    return d.get(key, None)

