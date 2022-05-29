from django import template
from decimal import Decimal



register = template.Library()


@register.filter(name='offer_price_start')
def offer_price_start(queryset):
    return queryset.first().price


@register.filter(name="cart_quantity")
def cart_quantity(package_id, cart):
    keys = cart.keys()
    for id in keys:
        if int(id) == package_id.id:
            return cart.get(id)
    return 0


@register.filter(name='cart_total')
def cart_total(package_id, cart):
    if package_id.price:
        return package_id.price * cart_quantity(package_id, cart)
    else:
        pass


#subtotal
@register.filter(name='get_subtotal_cart_total')
def get_subtotal_cart_total(package_id, cart):
	subtotal = 0
	for p in package_id:
		subtotal += cart_total(p, cart)
	return subtotal




@register.filter(name="total_with_service_fee")
def get_total_with_service_fee(package_id, cart):
    total = 0
    service_fee = 0
    for p in package_id:
        total1 = cart_total(p, cart)
        service = total1 * 5 / 100
        total += total1 + Decimal(service)
    return total