from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.datetime_safe import datetime
from parameterized import parameterized
from wagtail.core.blocks import CharBlock
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.blocks import RichTextBlock
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtail.core.blocks import StructValue
from wagtail.core.rich_text import RichText
from wagtailmarkdown.blocks import MarkdownBlock

from blog.constants import INTRO_ELLIPSIS
from blog.constants import ArticleBodyBlockNames
from blog.factories import ImageFactory
from blog.models import BlogArticlePage
from blog.models import CaptionedImageBlock
from blog.templatetags.blog_article_page_filters import add_slash
from blog.templatetags.blog_article_page_filters import is_pagination_suffix
from blog.templatetags.blog_article_page_filters import shorten_text
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
        [("title", None), ("page_title", None), ("date", None), ("author", None), ("read_time", -1), ("views", -1)]
    )
    def test_that_new_article_page_should_has_all_mandatory_parameters(self, parameter_name, parameter_value):
        author = BossFactory()
        body_block = StreamBlock([(ArticleBodyBlockNames.PARAGRAPH.value, RichTextBlock())])
        body = StreamValue(body_block, [(ArticleBodyBlockNames.PARAGRAPH.value, RichText("Hello, World"))])
        test_title = "Simple Article Title"
        blog_article_parameter = {
            "title": test_title,
            "page_title": test_title,
            "date": datetime.now(),
            "body": body,
            "author": author,
            "read_time": 7,
            "views": 0,
            parameter_name: parameter_value,
        }
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
        body_block = StreamBlock([(ArticleBodyBlockNames.PARAGRAPH.value, RichTextBlock())])
        body = StreamValue(body_block, [(ArticleBodyBlockNames.PARAGRAPH.value, RichText("Hello, World"))])
        test_title = "Simple Article Title"
        blog_article_parameter = {
            "title": test_title,
            "page_title": test_title,
            "date": datetime.now(),
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
            title="Simple Article Title", date=datetime(year=2019, month=5, day=1), read_time=5,
        )
        new_title = "Not So Simple Article Title"
        expected_slug = "simple-article-title"

        blog_article_page.title = new_title
        blog_article_page.save()

        self.assertEqual(blog_article_page.title, new_title)
        self.assertEqual(blog_article_page.slug, expected_slug)

    def test_that_deleting_recommended_articles_should_not_raise_any_errors(self):
        articles = [self._create_blog_article_page() for _ in range(3)]
        articles_block = StreamBlock([("page", PageChooserBlock())])
        recommended_articles = StreamValue(articles_block, [("page", article) for article in articles])
        main_article = self._create_blog_article_page(recommended_articles=recommended_articles)

        for article in articles:
            article.delete()
        main_article.refresh_from_db()

        self.assertEqual(BlogArticlePage.objects.all().count(), 1)
        self.assertEqual(len(main_article.recommended_articles), 0)

    def test_that_article_intro_should_be_a_part_of_first_paragraph_under_fixed_amount_of_characters(self):
        paragraph_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam laoreet venenatis enim, non luctus nisi finibus ut. Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat. Nulla ut purus elementum, auctor orci eget, facilisis est."
        expected_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam laoreet venenatis enim, non luctus nisi finibus ut. Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat. Nulla ut"

        body_block = StreamBlock([(ArticleBodyBlockNames.PARAGRAPH.value, RichTextBlock())])
        body = StreamValue(body_block, [(ArticleBodyBlockNames.PARAGRAPH.value, RichText(paragraph_string))])
        blog_article = self._create_blog_article_page(body=body)

        self.assertEqual(blog_article.intro, expected_string + INTRO_ELLIPSIS)

    def test_that_article_intro_should_take_multiple_paragraphs_under_account(self):
        paragraph_1 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam laoreet venenatis enim, non luctus nisi finibus ut."
        paragraph_2 = "Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat."
        paragraph_3 = "Nulla ut purus elementum, auctor orci eget, facilisis est. Nullam aliquet volutpat massa, vel bibendum libero venenatis ut. Integer ac sapien et urna sollicitudin."
        expected_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam laoreet venenatis enim, non luctus nisi finibus ut. Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat. Nulla ut"

        body_block = StreamBlock([(ArticleBodyBlockNames.PARAGRAPH.value, RichTextBlock())])
        body = StreamValue(
            body_block,
            [
                (ArticleBodyBlockNames.PARAGRAPH.value, RichText(paragraph_1)),
                (ArticleBodyBlockNames.PARAGRAPH.value, RichText(paragraph_2)),
                (ArticleBodyBlockNames.PARAGRAPH.value, RichText(paragraph_3)),
            ],
        )
        blog_article = self._create_blog_article_page(body=body)

        self.assertEqual(blog_article.intro, expected_string + INTRO_ELLIPSIS)

    def test_that_article_intro_should_support_markdown_blocks(self):
        paragraph_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam laoreet venenatis enim, non luctus nisi finibus ut. Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat. Nulla ut purus elementum, auctor orci eget, facilisis est."
        expected_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam laoreet venenatis enim, non luctus nisi finibus ut. Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat. Nulla ut"

        body_block = StreamBlock([(ArticleBodyBlockNames.MARKDOWN.value, MarkdownBlock())])
        body = StreamValue(body_block, [(ArticleBodyBlockNames.MARKDOWN.value, paragraph_string)])
        blog_article = self._create_blog_article_page(body=body)

        self.assertEqual(blog_article.intro, expected_string + INTRO_ELLIPSIS)

    def test_that_article_intro_should_strip_markdown_syntax(self):
        paragraph_string = "###Lorem ipsum `dolor` sit amet, **consectetur** adipiscing [elit](http://www.google.com). \r\n* Nullam *laoreet* venenatis enim, non luctus nisi finibus ut.\r\n> Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat. Nulla ut"
        expected_string = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam laoreet venenatis enim, non luctus nisi finibus ut. Mauris porta eleifend massa, nec maximus lacus luctus a. Aenean libero felis, placerat non malesuada a, maximus id erat. Nulla ut"

        body_block = StreamBlock([(ArticleBodyBlockNames.MARKDOWN.value, MarkdownBlock())])
        body = StreamValue(body_block, [(ArticleBodyBlockNames.MARKDOWN.value, paragraph_string)])
        blog_article = self._create_blog_article_page(body=body)

        self.assertEqual(blog_article.intro, expected_string + INTRO_ELLIPSIS)

    def test_that_image_caption_should_be_displayed_when_provided(self):
        caption_text = "Test caption"
        body_block = StreamBlock([("image", CaptionedImageBlock())])
        block_value = StructValue(CaptionedImageBlock, [("image", ImageFactory()), ("caption", caption_text)])
        body = StreamValue(body_block, [("image", block_value)])
        blog_article_page = self._create_blog_article_page(body=body)

        response = self.client.get(path=blog_article_page.get_absolute_url())

        self.assertContains(response, caption_text)

    def test_that_article_should_be_properly_rendered_if_image_has_no_caption(self):
        body_block = StreamBlock([("image", CaptionedImageBlock())])
        block_value = StructValue(CaptionedImageBlock, [("image", ImageFactory()), ("caption", "")])
        body = StreamValue(body_block, [("image", block_value)])
        blog_article_page = self._create_blog_article_page(body=body)

        response = self.client.get(path=blog_article_page.get_absolute_url())

        self.assertEqual(response.status_code, 200)


class TestBlogArticleTableOfContents(TestCase, BlogTestHelpers):
    def setUp(self):
        self._set_default_blog_index_page_as_new_root_page_child()
        self.blog_index_page = self._get_newest_blog_index_page()
        header_block = StreamBlock([(ArticleBodyBlockNames.HEADER.value, CharBlock())])
        body = StreamValue(
            header_block,
            [
                (ArticleBodyBlockNames.HEADER.value, "Header 1"),
                (ArticleBodyBlockNames.HEADER.value, "Header 2"),
                (ArticleBodyBlockNames.HEADER.value, "Header 3"),
            ],
        )
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


class TestBlogPageFilters(TestCase):
    def test_that_shorten_text_filter_should_return_empty_string_when_text_argument_is_empty(self):
        returned_text = shorten_text("", 100)
        expected_result = ""

        self.assertEqual(returned_text, expected_result)

    @parameterized.expand([("Hello World!", 100), ("Hello World!", 8)])
    def test_that_length_of_returned_string_by_shorten_text_filter_should_be_less_or_equal_to_specified_length(
        self, text, max_length_of_string
    ):
        length_of_returned_text = len(shorten_text(text, max_length_of_string))

        self.assertLessEqual(length_of_returned_text, max_length_of_string)

    @parameterized.expand([("Hello World!", 8, "Hello..."), ("Hello World!", 4, "...")])
    def test_that_returned_string_by_shorten_text_filter_should_not_contain_cut_words(
        self, text, max_length_of_string, expected_result
    ):
        returned_text = shorten_text(text, max_length_of_string)

        self.assertEqual(returned_text, expected_result)

    @parameterized.expand([("Hello World!", 100), ("Hello World!", 12)])
    def test_that_shorten_text_filter_should_return_same_string_when_length_of_string_is_less_than_or_equal_to_max(
        self, text, max_length_of_string
    ):
        returned_text = shorten_text(text, max_length_of_string)

        self.assertEqual(returned_text, text)

    def test_that_add_slash_filter_should_add_slash_at_the_end_of_path_when_missing_one(self):
        path = "blog/article-name-here"
        expected_result = f"{path}/"

        returned_path = add_slash(path)

        self.assertEqual(returned_path, expected_result)

    def test_that_add_slash_filter_should_not_add_slash_at_the_end_of_path_when_occur(self):
        path = "blog/article-name-here/"

        returned_path = add_slash(path)

        self.assertEqual(returned_path, path)

    def test_that_is_pagination_suffix_filter_should_return_true_if_pagination_suffix_occur_in_path(self):
        path = "blog/?page=1"

        returned_value = is_pagination_suffix(path)

        self.assertTrue(returned_value)

    def test_that_is_pagination_suffix_filter_should_return_false_if_pagination_suffix_does_not_occur_in_path(self):
        path = "blog/"

        returned_value = is_pagination_suffix(path)

        self.assertFalse(returned_value)
