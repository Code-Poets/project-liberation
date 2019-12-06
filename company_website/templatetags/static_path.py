from django import template
from django.conf import settings
from django.contrib.sites.models import Site
from django.templatetags.static import static

register = template.Library()


@register.filter("get_static_url")
def get_static_url(static_path: str) -> str:
    return f"{settings.URL_PREFIX}://{Site.objects.get_current().domain}{static(static_path)}"
