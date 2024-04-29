from atexit import register
from django import template

register = template.Library()

@register.filter(name='currency')
def currency(number):
    return "₹"+ str(number)

@register.filter(name='multiply')
def multiply(number, number2):
    return number*number2