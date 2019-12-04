from django.test import TestCase

from blog.models import BlogArticlePage
from blog.tests.test_helpers import BlogTestHelpers


class TestBlogIndexPageIntegration(TestCase, BlogTestHelpers):
    def setUp(self) -> None:
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_category_snippet = self._create_blog_category_snippet()
        self.number_of_articles = 4
        for loop_number in range(self.number_of_articles):
            self._create_blog_article_page(views=loop_number)
        self.blog_index_page = self._get_newest_blog_index_page()

    def test_that_get_all_articles_method_should_return_all_blog_article_page_objects(self):
        article_list = self.blog_index_page.get_all_articles()
        self.assertEqual(len(article_list), self.number_of_articles)

    def test_that_get_main_article_method_should_return_main_article(self):
        main_article = self.blog_index_page.get_main_article()
        self.assertIsInstance(main_article, BlogArticlePage)
        self.assertEqual(main_article.is_main_article, True)

    def test_that_get_rest_articles_method_should_return_all_articles_but_main_article(self):
        rest_articles = self.blog_index_page.get_rest_articles()
        self.assertEqual(len(rest_articles), self.number_of_articles - 1)
        for article in rest_articles:
            self.assertEqual(article.is_main_article, False)

    def test_that_get_popular_articles_should_return_most_popular_blog_articles(self):
        popular_articles = self.blog_index_page.get_popular_articles()
        self.assertEqual(len(popular_articles), 3)
        most_views = popular_articles[0].views
        for article in popular_articles:
            self.assertEqual(article.views, most_views)
            most_views -= 1
