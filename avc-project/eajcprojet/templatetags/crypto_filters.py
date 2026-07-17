from django import template
from eajcprojet.utils.crypto import chiffrer_param

register = template.Library()

@register.filter
def crypter_id(value):
    return chiffrer_param(str(value))
