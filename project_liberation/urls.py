from django.conf.urls import url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include

from blog.sitemap import BlogArticlesSitemap
from blog.sitemap import BlogCategorySitemap
from blog.sitemap import BlogIndexSitemap
from company_website.sitemap import CompanyWebsiteViewSitemap
from project_liberation.views import redirect_view

sitemaps = {
    "company_website": CompanyWebsiteViewSitemap,
    "blog_index_page": BlogIndexSitemap,
    "blog_categories": BlogCategorySitemap,
    "blog_articles": BlogArticlesSitemap,
}


urlpatterns = [
    # sitemaps
    url("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    # robots.txt
    url(r"^robots.txt", include("robots.urls")),
    # company website urls
    url(r"^admin/", admin.site.urls),
    url(r"^", include("company_website.urls")),
    # blog urls
    url(r"^blog/", include("blog.urls")),
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
    # google analytics url
    url(r"^djga/", include("google_analytics.urls")),
]
