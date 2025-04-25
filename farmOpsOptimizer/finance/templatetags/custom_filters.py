from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    """Multiplies value by arg and returns the result."""
    try:
        # Ensure both value and arg are numeric types
        return float(value) * float(arg)
    except (TypeError, ValueError):
        return 0  # Return 0 if there is any error in conversion
