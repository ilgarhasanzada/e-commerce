from django import template
from shop.models import Product

register = template.Library()


@register.filter
def is_wished(product, request):
    return product in Product.objects.filter(favorite_products__customer=request.user.customer)