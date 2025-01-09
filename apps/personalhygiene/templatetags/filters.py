# templatetags/filters.py

import re
from django import template

register = template.Library()

@register.filter
def replace_yes_no(value):
    if value:
        # Use regular expressions to replace whole words "yes" and "no" with <b>yes</b><br> and <b>no</b><br>
        value = re.sub(r'\bYes\b', '<b>Yes</b><br>', value)
        value = re.sub(r'\bNo\b', '<b>No</b><br>', value)
    return value


@register.filter
def replace_list_bracket(value):
    if value:
        value = re.sub(r"\['", "", value)
        value = re.sub(r"'\]", "\n", value)
    return value
