from typing import Any

from django import template

register = template.Library()


@register.simple_tag
def define_variable(value: Any = None) -> Any:
    return value
