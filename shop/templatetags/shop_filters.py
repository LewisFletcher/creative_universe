from django import template

register = template.Library()

@register.filter
def cart_count(cart):
    return sum(cart.values()) if cart else 0

@register.filter
def in_cart(item, cart):
    item_key = f"{item.get_model_name()}_{item.id}"
    return item_key in cart

@register.filter
def mul(value, arg):
    """Multiplies the value by the arg."""
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''