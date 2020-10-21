from django.test import TestCase
from wagtail.core.models import Page

from blog.factories import BlogArticlePageFactory
from blog.factories import BlogIndexPageFactory
from blog.models import BlogIndexPage


class BlogArticlePageFactoryTests(TestCase):
    def test_that_blog_article_page_should_have_the_same_parent_as_specified(self):
        BlogIndexPageFactory(title="First Index Page")
        blog_index_page = BlogIndexPageFactory(title="Second Index Page")
        blog_article_page = BlogArticlePageFactory(parent=blog_index_page)

        self.assertEqual(blog_article_page.get_parent(), blog_index_page)

    def test_that_blog_article_page_factory_should_create_new_blog_index_page_if_none_exist(self):
        BlogArticlePageFactory()

        self.assertEqual(BlogIndexPage.objects.all().count(), 1)

    def test_that_blog_article_page_should_have_the_first_blog_index_page_as_parent_if_none_is_specified(self):
        blog_index_page = BlogIndexPageFactory(title="First Index Page")
        BlogIndexPageFactory(title="Second Index Page")

        blog_article_page = BlogArticlePageFactory()

        self.assertEqual(blog_article_page.get_parent(), blog_index_page)


class BlogIndexPageFactoryTests(TestCase):
    def test_that_blog_index_page_should_be_parent_of_root_by_default(self):
        blog_index_page = BlogIndexPageFactory(title="Blog Index Page")

        self.assertEqual(blog_index_page.get_parent(), Page.objects.get(title="Root"))
