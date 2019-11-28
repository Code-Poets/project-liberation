from django.test import TestCase
from wagtail.core.models import Page

from blog.models import BlogIndexPage
from blog.tests.test_helpers import BlogTestHelpers


class TestBlogIndexPage(TestCase, BlogTestHelpers):
    def test_that_blog_index_page_can_be_child_of_root_page(self):
        root_page = Page.objects.get(title="Root")
        blog_index_page = self._add_blog_index_page_as_root_child_page()
        self.assertEqual(blog_index_page.get_parent(), root_page)

    def test_that_blog_index_page_as_root_page_in_site_will_work(self):
        (blog_index_page, site) = self._set_default_blog_index_page_as_new_root_page_child()
        self.assertEqual(site.root_page, blog_index_page)
        response = self.client.get(self.blog_index_page_url)
        self.assertTemplateUsed(response, BlogIndexPage.template)
