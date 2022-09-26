from django import template
from django.utils import timezone

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):                     # replace value of a param in current url
    d = context['request'].GET.copy()                   # need for switching pages without resetting filters
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag(takes_context=True)                # add timezone to context so we could alter theme using only this tag in default.html
def current_time(context, **kwargs):
    context['current_time'] = timezone.now()
    return ''                                           # return empty string, so there would be no None in default.html

