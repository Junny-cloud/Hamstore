import locale
from django import template
from django import template
register = template.Library()


@register.filter
def cfa(value):
    locale.setlocale(locale.LC_ALL, 'fr_FR.utf-8')
    return "{:0,.0f}".format(value).replace(',','.')


@register.filter
def format_phone_number(value):
    formatted_string = " ".join([value[i:i+2] for i in range(0, len(value), 2)])
    return formatted_string


@register.filter
def format_date(value):
    formatted_date = value.strftime("%d %b %y")
    return formatted_date
