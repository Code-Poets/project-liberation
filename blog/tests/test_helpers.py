from django.urls import reverse
from wagtail.core.models import Page
from wagtail.core.models import Site

from blog.models import BlogCategoryPage
from blog.models import BlogCategorySnippet
from blog.models import BlogIndexPage


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
