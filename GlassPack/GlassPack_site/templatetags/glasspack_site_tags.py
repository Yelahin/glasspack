from django import template
from ..models import Product

register = template.Library()

@register.filter
def type_select(value, arg):
    if not isinstance(value, list):
        value = list(value)
    result = value.copy()
    if arg in result:
        result.remove(arg)
    else:
        result.append(arg)
    if len(result) < 1:
        result = ['bottles', 'jars']
    return ','.join(result)


@register.filter
def finish_param(selected_finish_types, finish_str):
    if selected_finish_types:
        return f"&finish_types={finish_str}"
    return ""