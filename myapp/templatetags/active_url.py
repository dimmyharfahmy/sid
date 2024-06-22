# myapp/templatetags/active_url.py

from django import template
from django.urls import resolve

register = template.Library()

@register.simple_tag
def active_url(request, view_name):
    if resolve(request.path_info).url_name == view_name:
        return 'active'
    return ''