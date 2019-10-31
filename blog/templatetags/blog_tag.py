from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def blog_url(path: str = None) -> str:
    return reverse("blog:company-blog:wagtail_serve", args=(path.replace(" ", "-").lower(),))
