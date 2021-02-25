import textwrap

from django import template

from blog.models import BlogArticlePage

register = template.Library()


@register.filter
def get_header_id(page: BlogArticlePage, title: str) -> int:
    return page.get_header_id(title)


@register.filter
def shorten_text(text: str, max_length: int) -> str:
    return textwrap.shorten(text, width=max_length, placeholder="...")


@register.filter
def add_slash(path: str) -> str:
    return f"{path}/" if path[-1] != "/" else path


@register.filter
def is_pagination_suffix(path: str) -> bool:
    return "?page=" in path
