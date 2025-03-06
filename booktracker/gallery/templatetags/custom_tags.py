from django import template

register = template.Library()

@register.filter
def dict_key(value, key):
    """Gibt den Wert für den angegebenen Schlüssel im Dictionary zurück."""
    if isinstance(value, dict):
        return value.get(key, None)
    return None