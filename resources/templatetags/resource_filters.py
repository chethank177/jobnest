from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """
    Custom template filter to get an item from a dictionary using a variable key
    Usage: {{ dictionary|get_item:key_variable }}
    """
    return dictionary.get(key, []) 