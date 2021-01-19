from typing import Any

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def define_variable(value: Any = None) -> Any:
    return value


@register.filter
@stringfilter
def is_webp_supported(browser_family: str) -> bool:
    browser_family = browser_family.lower()
    is_supported = all(["ie" not in browser_family, "safari" not in browser_family])

    return is_supported
