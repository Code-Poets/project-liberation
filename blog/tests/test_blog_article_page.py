from django.core.exceptions import ValidationError
from django.test import TestCase

from blog.models import BlogCategoryPage
from blog.tests.test_helpers import BlogTestHelpers


class TestBlogArticlePage(TestCase, BlogTestHelpers):
    def setUp(self) -> None:
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_category = self._create_blog_category_snippet()
        self.blog_category_page = BlogCategoryPage.objects.get(**self.blog_category.instance_parameters)
        self.blog_index_page = self._get_newest_blog_index_page()

    def test_that_new_article_page_can_be_only_index_blog_page_child(self):
        blog_article_page = self._create_blog_article_page()
        with self.assertRaises(ValidationError):
            self._create_blog_article_page(blog_index_page=blog_article_page)

    def test_that_new_article_page_should_has_all_mandatory_parameters(self):
        pass

    def test_that_first_article_should_be_main_article(self):
        pass

    def test_that_every_article_page_opening_should_raise_view_counter(self):
        pass

    def test_that_making_one_article_as_main_article_should_change_main_article_flag_in_article_which_was_main(self):
        pass
