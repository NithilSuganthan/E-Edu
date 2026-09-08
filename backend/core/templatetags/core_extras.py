
from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # Tolerate missing/empty context values (e.g. progress_map absent for
    # unauthenticated or non-enrolled visitors) instead of raising AttributeError.
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
