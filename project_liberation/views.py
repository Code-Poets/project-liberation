from django.contrib.sites.shortcuts import get_current_site
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseRedirect


def redirect_view(request: WSGIRequest, **kwargs: dict) -> HttpResponseRedirect:
    domain = get_current_site(request)
    blog_article_address = kwargs["blog_article_address"]
    return HttpResponseRedirect(f"https://{domain}/blog/{blog_article_address}")
