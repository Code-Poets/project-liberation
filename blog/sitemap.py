from wagtail.core.query import PageQuerySet

from blog.models import BlogArticlePage
from blog.models import BlogIndexPage
from common.custom_sitemap import CustomSitemap


class BlogIndexSitemap(CustomSitemap):
    def items(self) -> PageQuerySet:
        return BlogIndexPage.objects.filter(live=True)


class BlogArticlesSitemap(CustomSitemap):
    def items(self) -> PageQuerySet:
        return BlogArticlePage.objects.filter(live=True)
