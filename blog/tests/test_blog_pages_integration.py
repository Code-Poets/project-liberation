import math

from django.test import TestCase
from django.utils.datetime_safe import datetime

from blog.models import BlogArticlePage
from blog.models import BlogIndexPage
from blog.tests.test_helpers import BlogTestHelpers


class TestBlogIndexPageIntegration(TestCase, BlogTestHelpers):
    def setUp(self) -> None:
        self._set_default_blog_index_page_as_new_root_page_child()
        self.number_of_articles = 6
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
        self.assertEqual(len(popular_articles), 5)
        most_views = popular_articles[0].views
        for article in popular_articles:
            self.assertEqual(article.views, most_views)
            most_views -= 1


class BlogSetUpClass(TestCase, BlogTestHelpers):
    def setUp(self) -> None:
        self._set_default_blog_index_page_as_new_root_page_child()
        self.articles_amount = 10
        self.articles = []
        self.custom_date = datetime(year=2019, month=1, day=1)
        for loop_number in range(1, self.articles_amount + 1):
            self.articles.append(
                self._create_blog_article_page(
                    title=f"Simple Article Title {loop_number}",
                    date=datetime(year=2019, month=loop_number, day=1),
                    intro=f"Simple Article Intro {loop_number}",
                    read_time=loop_number,
                )
            )


class TestBlogPagesPagination(BlogSetUpClass):
    def test_that_pagination_in_displayed_on_index_page_when_is_more_than_6_articles(self):
        response = self.client.get(self.blog_index_page_url)
        number_of_paginated_pages = math.ceil(BlogArticlePage.objects.all().count() / 6)
        self.assertTemplateUsed(response, BlogIndexPage.template)
        for number in range(1, number_of_paginated_pages + 1):
            self.assertIn(f"?page={number}", response.rendered_content)


class TestBlogPagesSlugFieldPreservation(TestCase, BlogTestHelpers):
    def setUp(self):
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_article_page = self._create_blog_article_page(
            title="Simple Article Title",
            date=datetime(year=2019, month=5, day=1),
            intro="Simple Article Intro",
            read_time=5,
        )
        self.new_title = "Not So Simple Article Title"
        self.expected_slug = "simple-article-title"

    def test_that_altering_title_in_blog_page_model_should_not_alter_the_url_slug(self):
        self.blog_article_page.title = self.new_title
        self.blog_article_page.save()

        self.assertEqual(self.blog_article_page.title, self.new_title)
        self.assertEqual(self.blog_article_page.slug, self.expected_slug)
