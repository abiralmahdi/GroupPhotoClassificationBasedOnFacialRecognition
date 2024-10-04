
from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def break_if(context, condition):
    context['break'] = condition
    return ''
