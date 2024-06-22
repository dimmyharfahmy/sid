# myapp/templatetags/form_extras.py

from django import template

register = template.Library()

@register.filter
def add_placeholder(field, placeholder_text):
    field.field.widget.attrs.update({'placeholder': placeholder_text})
    return field
