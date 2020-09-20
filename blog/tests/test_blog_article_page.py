from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.datetime_safe import datetime
from parameterized import parameterized
from wagtail.core.blocks import CharBlock
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtailmarkdown.blocks import MarkdownBlock

from blog.models import MAX_BLOG_ARTICLE_TITLE_LENGTH
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
        body_block = StreamBlock([("markdown", MarkdownBlock())])
        body = StreamValue(body_block, [("markdown", "Hello, World")])
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

    def test_that_title_should_not_be_longer_than_custom_specified_amount_of_characters(self):
        title_that_is_way_too_long = "f" * (MAX_BLOG_ARTICLE_TITLE_LENGTH + 1)
        with self.assertRaises(ValidationError):
            self._create_blog_article_page(title=title_that_is_way_too_long)

    def test_that_recommended_articles_should_not_contain_duplicates(self):
        other_article = self._create_blog_article_page()
        articles_block = StreamBlock([("page", PageChooserBlock())])
        recommended_articles_with_duplicates = StreamValue(
            articles_block, [("page", other_article), ("page", other_article)]
        )
        with self.assertRaises(ValidationError):
            self._create_blog_article_page(recommended_articles=recommended_articles_with_duplicates)

    def test_that_existing_article_should_not_be_given_duplicated_article_in_recommendations(self):
        other_article = self._create_blog_article_page()
        articles_block = StreamBlock([("page", PageChooserBlock())])
        recommended_articles = StreamValue(articles_block, [("page", other_article)])
        article = self._create_blog_article_page(recommended_articles=recommended_articles)
        article.recommended_articles.stream_data.append(("page", other_article))
        with self.assertRaises(ValidationError):
            article.full_clean()

    def test_that_article_with_no_recommended_articles_should_be_valid(self):
        author = BossFactory()
        body_block = StreamBlock([("markdown", MarkdownBlock())])
        body = StreamValue(body_block, [("markdown", "Hello, World")])
        blog_article_parameter = {
            "title": "Simple Article Title",
            "date": datetime.now(),
            "intro": "Simple Article Intro",
            "body": body,
            "author": author,
            "read_time": 7,
            "views": 0,
        }
        articles_block = StreamBlock([("page", PageChooserBlock())])

        blog_article_page = BlogArticlePage(**blog_article_parameter)
        self.blog_index_page.add_child(instance=blog_article_page)
        blog_article_page.save()

        self.assertEqual(blog_article_page.recommended_articles, StreamValue(articles_block, []))

    def test_that_altering_title_in_blog_page_model_should_not_alter_the_url_slug(self):
        blog_article_page = self._create_blog_article_page(
            title="Simple Article Title",
            date=datetime(year=2019, month=5, day=1),
            intro="Simple Article Intro",
            read_time=5,
        )
        new_title = "Not So Simple Article Title"
        expected_slug = "simple-article-title"

        blog_article_page.title = new_title
        blog_article_page.save()

        self.assertEqual(blog_article_page.title, new_title)
        self.assertEqual(blog_article_page.slug, expected_slug)


class TestBlogArticleTableOfContents(TestCase, BlogTestHelpers):
    def setUp(self):
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_index_page = self._get_newest_blog_index_page()
        header_block = StreamBlock([("header", CharBlock())])
        body = StreamValue(header_block, [("header", "Header 1"), ("header", "Header 2"), ("header", "Header 3")])
        self.blog_article_page = self._create_blog_article_page(
            blog_index_page=self.blog_index_page, body=body, table_of_contents=True
        )

    def test_that_headers_list_property_should_return_list_of_all_headers(self):
        expected_result = ["Header 1", "Header 2", "Header 3"]
        self.assertEqual(self.blog_article_page.headers_list, expected_result)

    @parameterized.expand([("Header 1", 0), ("Header 2", 1), ("Header 3", 2)])
    def test_that_get_header_id_should_return_integer_representing_header_ordering_number(self, header, expected_id):
        self.assertEqual(self.blog_article_page.get_header_id(header), expected_id)

    def test_that_blog_article_page_should_display_table_of_contents_containing_all_headers(self):
        expected_data = {0: "Header 1", 1: "Header 2", 2: "Header 3"}

        response = self.client.get(path=self.blog_article_page.get_absolute_url())

        self.assertContains(response, "Table of contents")
        for (header_id, header) in expected_data.items():
            self.assertContains(response, header)
            self.assertContains(response, f"href='#{header_id}'")
            self.assertContains(response, f"id='{header_id}'")

    def test_that_article_page_should_not_display_table_of_contents_if_field_is_set_to_false(self):
        self.blog_article_page.table_of_contents = False
        self.blog_article_page.full_clean()
        self.blog_article_page.save()
        response = self.client.get(path=self.blog_article_page.get_absolute_url())

        self.assertNotContains(response, "Table of contents")

    def test_that_table_of_contents_should_be_set_to_false_if_there_are_no_headers(self):
        other_article = self._create_blog_article_page(blog_index_page=self.blog_index_page)

        other_article.table_of_contents = True
        other_article.full_clean()

        self.assertTrue(other_article.table_of_contents)

        other_article.save()

        self.assertFalse(other_article.table_of_contents)


class TestBlogArticlePageMainArticleIntegrity(TestCase, BlogTestHelpers):
    def setUp(self):
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_index_page = self._get_newest_blog_index_page()
        self.article = self._create_blog_article_page(is_main_article=True)

    def test_that_setting_main_article_flag_to_true_should_make_the_article_the_new_main_article(self):
        other_article = self._create_blog_article_page(is_main_article=True)
        self.article.refresh_from_db()

        self.assertTrue(other_article.is_main_article)
        self.assertFalse(self.article.is_main_article)

    def test_that_if_main_article_flag_is_set_to_false_it_should_be_switched_back_to_true_after_saving(self):
        self.article.is_main_article = False
        self.article.save()

        self.assertTrue(self.article.is_main_article)

    def test_that_if_main_article_is_deleted_the_latest_article_should_be_marked_as_the_main_article(self):
        older_article = self._create_blog_article_page(date=datetime.now().date() + relativedelta(days=-2))
        newer_aticle = self._create_blog_article_page(date=datetime.now().date() + relativedelta(days=-1))

        self.article.delete()
        older_article.refresh_from_db()
        newer_aticle.refresh_from_db()

        self.assertFalse(older_article.is_main_article)
        self.assertTrue(newer_aticle.is_main_article)

    def test_that_when_deleting_main_article_only_one_other_article_can_become_the_main_article(self):
        for _ in range(2):
            self._create_blog_article_page(date=datetime.now() + relativedelta(days=-1))

        self.article.delete()

        self.assertEqual(BlogArticlePage.objects.filter(is_main_article=True).count(), 1)

    def test_that_removing_main_article_should_be_possible_if_there_are_no_other_articles(self):
        self.article.delete()
        self.assertEqual(BlogArticlePage.objects.all().count(), 0)
