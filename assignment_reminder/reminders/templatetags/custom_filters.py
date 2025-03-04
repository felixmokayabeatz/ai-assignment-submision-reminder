# from django import template

# register = template.Library()

# @register.filter
# def dict_get(dictionary, key):
#     """Custom template filter to get a dictionary value by key."""
#     return dictionary.get(key, None)


# from django import template

from django import template

register = template.Library()
register = template.Library()

@register.filter
def dict_get(dictionary, key):
    """Returns the value from a dictionary for the given key."""
    return dictionary.get(key)



@register.filter
def dict_key(dictionary, key):
    """Retrieve a value from a dictionary using a key in Django templates."""
    return dictionary.get(key)
