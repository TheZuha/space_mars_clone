from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def discount_price(value, discount):
    try:
        value = Decimal(value)
        discount = Decimal(discount)
    except (ValueError, TypeError):
        return value

    if discount:
        discounted_price = value * (1 - discount / Decimal(100))
        return "{:.0f}".format(discounted_price)
    return "{:.0f}".format(value)

@register.filter
def format_price(value):
    try:
        value = int(value)
        return "{:,.0f}".format(value).replace(',', ' ')
    except (ValueError, TypeError):
        return value