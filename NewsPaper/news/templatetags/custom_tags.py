from datetime import datetime
from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):                     # replace value of a param in current url
    d = context['request'].GET.copy()                   # need for switching pages without resetting filters
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag()
def current_time(format_string='%b %d %Y'):
    return datetime.utcnow().strftime(format_string)
