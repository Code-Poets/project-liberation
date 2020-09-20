from django import template

from blog.models import BlogArticlePage

register = template.Library()


@register.filter
def get_header_id(page: BlogArticlePage, title: str) -> int:
    return page.get_header_id(title)
