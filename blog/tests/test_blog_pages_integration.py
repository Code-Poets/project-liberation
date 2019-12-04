from django.test import TestCase
from django.utils.datetime_safe import datetime

from blog.models import BlogArticlePage
from blog.models import BlogCategoryPage
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


class TestBlogCategoryPageIntegration(TestCase, BlogTestHelpers):
    def setUp(self) -> None:
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_category_1 = self._create_blog_category_snippet(title="Test Category", slug="test-category")
        self.blog_category_2 = self._create_blog_category_snippet(title="Test Category 2", slug="test-category-2")
        self.blog_category_1_articles_amount = 3
        self.blog_category_2_articles_amount = 5
        self.blog_category_1_articles = []
        self.blog_category_2_articles = []
        self.custom_date = datetime(year=2019, month=1, day=1)
        for loop_number in range(1, self.blog_category_1_articles_amount + 1):
            self.blog_category_1_articles.append(
                self._create_blog_article_page(
                    categories=[self.blog_category_1],
                    title=f"Simple Article Title {self.blog_category_1.title} {loop_number}",
                    date=datetime(year=2019, month=loop_number, day=1),
                    intro=f"Simple Article Intro {self.blog_category_1.title} {loop_number}",
                    read_time=loop_number,
                )
            )
        for loop_number in range(1, self.blog_category_2_articles_amount + 1):
            self.blog_category_2_articles.append(
                self._create_blog_article_page(
                    categories=[self.blog_category_2],
                    title=f"Simple Article Title {self.blog_category_2.title} {loop_number}",
                    date=datetime(year=2019, month=loop_number, day=2),
                    intro=f"Simple Article Intro {self.blog_category_2.title} {loop_number}",
                    read_time=loop_number,
                )
            )

    def test_that_category_page_should_show_articles_which_are_related_only_with_this_category(self):
        response = self.client.get(BlogCategoryPage.objects.get(**self.blog_category_1.instance_parameters).full_url)
        self.assertTemplateUsed(response, BlogCategoryPage.template)
        for category_1_article in self.blog_category_1_articles:
            self.assertIn(category_1_article.title, response.rendered_content)
            self.assertIn(category_1_article.intro, response.rendered_content)
            self.assertIn(category_1_article.date.strftime("%b. %d, %Y"), response.rendered_content)
            self.assertIn(f"{category_1_article.read_time} min read", response.rendered_content)
            for category in category_1_article.categories.all():
                self.assertIn(category.title, response.rendered_content)
        for category_2_article in self.blog_category_2_articles:
            self.assertNotIn(category_2_article.title, response.rendered_content)
            self.assertNotIn(category_2_article.intro, response.rendered_content)
            self.assertNotIn(category_2_article.date.strftime("%b. %d, %Y"), response.rendered_content)
