from django import template
from django.utils.translation import gettext
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='replace')
def replace(value, args_string):
    args = args_string.split(',')
    value = value.replace(args[0], args[1])
    return value


@register.filter(name='translate')
def translate(text, arg):
    title = gettext(text)
    return title % arg


@register.filter(name='startswith')
def startswith(text, substring):
    return text.startswith(substring)


@register.filter(name='count')
def count(text, substring):
    return text.count(substring)


@register.simple_block_tag
def replace(content, *args):
    for arg in args:
        arg = arg.split(',')
        content = content.replace(arg[0], arg[1])
    return mark_safe(content)
