from django.urls import reverse
from django.utils.datetime_safe import datetime
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtail.core.models import Page
from wagtail.core.models import Site
from wagtailmarkdown.blocks import MarkdownBlock

from blog.models import BlogArticlePage
from blog.models import BlogCategoryPage
from blog.models import BlogCategorySnippet
from blog.models import BlogIndexPage
from company_website.factories import BossFactory


class BlogTestHelpers:

    # Blog main address
    blog_index_page_url = reverse("wagtail_serve", args=[""])

    # Blog Index page variables
    index_page_title = "Blog"
    index_page_description = "Blog meta description"
    index_page_keywords = "blog, keywords, test keywords"

    def _add_blog_index_page_as_root_child_page(
        self, title=index_page_title, meta_description=index_page_description, keywords=index_page_keywords
    ):  # pylint: disable=no-self-use
        blog_index_page = BlogIndexPage(title=title, meta_description=meta_description, keywords=keywords)
        Page.objects.get(title="Root").add_child(instance=blog_index_page)
        blog_index_page.save()
        return blog_index_page

    def _add_blog_index_page_as_site_root_page(self, blog_index_page):  # pylint: disable=no-self-use
        site = Site.objects.all().first()
        site.root_page = blog_index_page
        site.save()
        return site

    def _set_default_blog_index_page_as_new_root_page_child(self):
        blog_index_page = self._add_blog_index_page_as_root_child_page()
        site = self._add_blog_index_page_as_site_root_page(blog_index_page)
        return (blog_index_page, site)

    @staticmethod
    def _create_blog_category_snippet(
        title="Test Category",
        seo_title="Page SEO title",
        slug="test-category",
        meta_description="This is test category page",
        keywords="Category, Page, Blog",
        order=None,
    ):
        blog_category_snippet = BlogCategorySnippet(
            title=title,
            seo_title=seo_title,
            slug=slug,
            order=order,
            meta_description=meta_description,
            keywords=keywords,
        )
        blog_category_snippet.save()
        return blog_category_snippet

    @staticmethod
    def _create_blog_category_page(
        blog_index_page,
        title="Test Category",
        seo_title="Page SEO title",
        slug="test-category",
        meta_description="This is test category page",
        keywords="Category, Page, Blog",
    ):
        blog_category_page = BlogCategoryPage(
            title=title, seo_title=seo_title, slug=slug, meta_description=meta_description, keywords=keywords
        )
        blog_index_page.add_child(instance=blog_category_page)
        blog_category_page.save()
        return blog_category_page

    def _create_blog_article_page(
        self,
        blog_index_page=None,
        title="Simple Article Title",
        categories=None,
        date=datetime.now(),
        intro="Simple Article Intro",
        body=None,
        author=None,
        read_time=7,
        views=0,
        cover_photo=None,
        article_photo=None,
        is_main_article=False,
    ):
        if categories is None:
            categories = [BlogCategorySnippet.objects.all().first()]
        if body is None:
            block = StreamBlock([("markdown", MarkdownBlock())])
            body = StreamValue(block, [("markdown", "Hello, World")])
        if author is None:
            author = BossFactory()
        blog_article_page = BlogArticlePage(
            title=title,
            categories=categories,
            date=date,
            intro=intro,
            body=body,
            author=author,
            read_time=read_time,
            views=views,
            cover_photo=cover_photo,
            article_photo=article_photo,
            is_main_article=is_main_article,
        )
        if blog_index_page is None:
            blog_index_page = self._get_newest_blog_index_page()
        blog_index_page.add_child(instance=blog_article_page)
        blog_article_page.save()
        return blog_article_page

    @staticmethod
    def _get_newest_blog_index_page():
        return BlogIndexPage.objects.get(id=Site.objects.get(is_default_site=True).root_page_id)
