from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.datetime_safe import datetime
from parameterized import parameterized
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtailmarkdown.blocks import MarkdownBlock

from blog.models import BlogArticlePage
from blog.tests.test_helpers import BlogTestHelpers
from company_website.factories import BossFactory


class TestBlogArticlePage(TestCase, BlogTestHelpers):
    def setUp(self) -> None:
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_index_page = self._get_newest_blog_index_page()

    def test_that_new_article_page_can_be_only_index_blog_page_child(self):
        blog_article_page = self._create_blog_article_page()
        with self.assertRaises(ValidationError):
            self._create_blog_article_page(blog_index_page=blog_article_page)

    @parameterized.expand(
        [("title", None), ("date", None), ("intro", None), ("author", None), ("read_time", -1), ("views", -1),]
    )
    def test_that_new_article_page_should_has_all_mandatory_parameters(self, parameter_name, parameter_value):
        author = BossFactory()
        block = StreamBlock([("markdown", MarkdownBlock())])
        body = StreamValue(block, [("markdown", "Hello, World")])
        blog_article_parameter = {
            "title": "Simple Article Title",
            "date": datetime.now(),
            "intro": "Simple Article Intro",
            "body": body,
            "author": author,
            "read_time": 7,
            "views": 0,
        }
        blog_article_parameter[parameter_name] = parameter_value
        with self.assertRaises(ValidationError):
            blog_article_page = BlogArticlePage(**blog_article_parameter)
            self.blog_index_page.add_child(instance=blog_article_page)
            blog_article_page.save()

    def test_that_first_article_should_be_main_article(self):
        blog_article_page = self._create_blog_article_page(is_main_article=False)
        self.assertEqual(blog_article_page.is_main_article, True)

    def test_that_every_article_page_opening_should_raise_view_counter(self):
        blog_article_page = self._create_blog_article_page()
        self.assertEqual(blog_article_page.views, 0)
        number_of_views = 5
        for _ in range(number_of_views):
            self.client.get(blog_article_page.full_url)
        self.assertEqual(BlogArticlePage.objects.get(pk=blog_article_page.pk).views, number_of_views)

    def test_that_making_one_article_as_main_article_should_change_main_article_flag_in_article_which_was_main(self):
        blog_article_page = self._create_blog_article_page(is_main_article=False)
        self.assertEqual(blog_article_page.is_main_article, True)
        blog_article_page_2 = self._create_blog_article_page(is_main_article=True)
        self.assertEqual(blog_article_page_2.is_main_article, True)
        self.assertEqual(BlogArticlePage.objects.get(pk=blog_article_page.pk).is_main_article, False)
