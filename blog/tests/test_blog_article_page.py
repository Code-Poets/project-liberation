from django.test import TestCase

from blog.tests.test_helpers import BlogTestHelpers


class TestBlogArticlePage(TestCase, BlogTestHelpers):
    def test_that_new_article_page_can_be_only_index_blog_page_child(self):
        pass

    def test_that_new_article_page_should_has_all_mandatory_parameters(self):
        pass

    def test_that_first_article_should_be_main_article(self):
        pass

    def test_that_every_article_page_opening_should_raise_view_counter(self):
        pass

    def test_that_making_one_article_as_main_article_should_change_main_article_flag_in_article_which_was_main(self):
        pass
