from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

# @register.simple_tag(takes_context=True)
# def active_url(context, url_name):
#     request = context['request']
#     try:
#         url = reverse(url_name)
#         if request.path == url:
#             return 'active'
#     except NoReverseMatch:
#         pass
#     return ''

@register.simple_tag(takes_context=True)
def active_url(context, view_name):
    request = context['request']
    try:
        url = reverse(view_name)
        if request.path == url:
            return 'active'
    except NoReverseMatch:
        pass
    return ''