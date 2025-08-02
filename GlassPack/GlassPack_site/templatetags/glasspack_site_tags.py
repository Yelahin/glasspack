from django import template
import GlassPack_site.views as views

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
