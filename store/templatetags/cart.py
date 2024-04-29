from urllib import request
from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product, cart):
    keys =  cart.keys()
    print(keys)
    print(product)
    for id in keys:
        if id == str(product.id):
            return True
    return False

@register.filter(name='cart_quantity')
def cart_quantity(product, cart):
    keys =  cart.keys()
    for e in keys:
        if e == str(product.id):
            return cart.get(e)
    return False

@register.filter(name='total_price')
def total_price(product, cart):
    total = product.price * cart_quantity(product, cart)
    
    return total

@register.filter(name='total_cart_price')
def total_cart_price(products, cart):
    sum=0
    if products:
        for p in products:
            sum += total_price(p, cart)
    
        return sum
    else:
        return None