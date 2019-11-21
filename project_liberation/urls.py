from django.conf.urls import url
from django.contrib import admin
from django.urls import include

from project_liberation.views import redirect_view

urlpatterns = [
    url(r"^admin/", admin.site.urls),
    url(r"^", include("company_website.urls")),
    url(r"^blog/", include("blog.urls")),
    url(r"^blog-cms/", include("blog.urls_admin")),
    # redirects for older blog posts
    url(
        r"^the-pycon-pl-2019-impressions/",
        redirect_view,
        kwargs={"blog_article_address": "the-pycon-pl-2019-impressions/"},
    ),
    url(r"^hello-world/", redirect_view, kwargs={"blog_article_address": "hello-world/"}),
    url(
        r"^ico-vs-sto-whats-best-for-your-startup/",
        redirect_view,
        kwargs={"blog_article_address": "ico-vs-sto-whats-best-for-your-startup/"},
    ),
    url(
        r"^how-prepare-your-mvp-idea-and-make-sure-your-customers-love-it/",
        redirect_view,
        kwargs={"blog_article_address": "how-prepare-your-mvp-idea-and-make-sure-your-customers-love-it/"},
    ),
    url(
        r"^code-poets-named-top-developers-poland/",
        redirect_view,
        kwargs={"blog_article_address": "code-poets-named-top-developers-poland/"},
    ),
]
