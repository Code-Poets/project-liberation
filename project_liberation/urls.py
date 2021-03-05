from django.conf.urls import url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include

from blog.sitemap import BlogArticlesSitemap
from blog.sitemap import BlogIndexSitemap
from company_website.sitemap import CompanyWebsiteViewSitemap

sitemaps = {
    "company_website": CompanyWebsiteViewSitemap,
    "blog_index_page": BlogIndexSitemap,
    "blog_articles": BlogArticlesSitemap,
}


urlpatterns = [
    # django admin
    url(r"^admin/", admin.site.urls),
    # company website urls
    url(r"^", include("company_website.urls")),
    # blog urls
    url(r"^blog/", include("blog.urls")),
]

# seo urls
urlpatterns += [
    url("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    url(r"^robots.txt", include("robots.urls")),
    url(r"^djga/", include("google_analytics.urls")),
]
