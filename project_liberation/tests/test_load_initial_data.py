from collections import Counter

import cv2
from django.test import TestCase
from parameterized import parameterized
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.blocks import StreamValue

from blog.factories import BlogArticlePageFactory
from blog.models import BlogArticlePage
from blog.models import BlogIndexPage
from blog.models import CustomImage
from company_website.factories import BossFactory
from company_website.factories import EmployeeFactory
from company_website.models import Employees
from company_website.models import Testimonial as ModelTestimonial
from project_liberation.management.commands.load_initial_data import Command as LoadInitialDataCommand


class LoadInitialDataTests(TestCase):
    def setUp(self):
        self.load_initial_data_command = LoadInitialDataCommand()

    def _assert_image_size_equal(self, image, height, width):
        self.assertEqual(image.shape[0], height)
        self.assertEqual(image.shape[1], width)

    def _assert_is_stream_value(self, stream_value, block_type, block_name):
        self.assertTrue(isinstance(stream_value, StreamValue))
        for stream_child in stream_value:
            self.assertTrue(isinstance(stream_child.block, block_type))
            self.assertEqual(stream_child.block.name, block_name)

    def _assert_wagtail_image_parameters_equal(self, wagtail_image, width, height, title):
        self.assertEqual(wagtail_image.title, title)
        image = cv2.imread(wagtail_image.file.path)
        self._assert_image_size_equal(image, height, width)

    def test_that_load_initial_data_should_create_fixed_amounts_of_objects(self):
        self.load_initial_data_command.bosses_limit = 2
        self.load_initial_data_command.employees_limit = 20
        self.load_initial_data_command.testimonial_limit = 5
        self.load_initial_data_command.articles_limit = 10

        self.load_initial_data_command.handle()

        self.assertEqual(Employees.objects.filter(boss=True).count(), 2)
        self.assertEqual(Employees.objects.filter(boss=False).count(), 20)
        self.assertEqual(ModelTestimonial.objects.all().count(), 5)
        self.assertEqual(BlogArticlePage.objects.all().count(), 10)
        self.assertEqual(BlogIndexPage.objects.all().count(), 1)

    @parameterized.expand([(True, 1, BossFactory, "Boss", 400, 267), (False, 3, EmployeeFactory, "Employee", 300, 200)])
    def test_that_add_employee_objects_should_generate_objects_with_provided_parameters(
        self, is_boss, limit, factory, employee_type, picture_height, picture_width
    ):
        self.load_initial_data_command._add_employee_objects(
            is_boss, limit, factory, employee_type, picture_height, picture_width
        )

        generated_employees = Employees.objects.all()

        self.assertEqual(generated_employees.count(), limit)
        for employee in generated_employees:
            self.assertEqual(employee.boss, is_boss)
            profile_pictures_set = [cv2.imread(employee.front_image.path), cv2.imread(employee.back_image.path)]
            for picture in profile_pictures_set:
                self._assert_image_size_equal(picture, picture_height, picture_width)

    def test_that_generate_article_data_should_generate_valid_data_for_blog_article_page_object(self):
        EmployeeFactory()

        article_data = self.load_initial_data_command._generate_article_data(1, Employees.objects.all())
        BlogArticlePageFactory(**article_data)

        self.assertEqual(len(article_data.items()), 4)
        self.assertEqual(article_data["author"], Employees.objects.all().first())
        self.assertTrue(article_data["is_main_article"])
        self.assertIsInstance(article_data["cover_photo"], CustomImage)
        self.assertIsInstance(article_data["article_photo"], CustomImage)

    def test_that_generate_recommended_articles_should_generate_valid_stream_of_articles_for_recommended_articles_field(
        self,
    ):
        for _ in range(10):
            BlogArticlePageFactory()

        for article in BlogArticlePage.objects.all():
            recommended_articles = self.load_initial_data_command._generate_recommended_articles(article.id)
            article.recommended_articles = recommended_articles

            self._assert_is_stream_value(recommended_articles, PageChooserBlock, "page")
            article.save()

    def test_that_generate_list_of_article_ids_for_recommended_articles_should_return_a_list_of_unique_ids_excluding_provided_target_id(
        self,
    ):
        for _ in range(20):
            BlogArticlePageFactory()

        for article in BlogArticlePage.objects.all():
            article_ids = self.load_initial_data_command._generate_list_of_article_ids_for_recommended_articles(
                article.id
            )

            self.assertTrue(article.id not in article_ids)
            ids_occurrences = Counter(article_ids)
            for occurrences in ids_occurrences.values():
                self.assertEqual(occurrences, 1)

    def test_that_generate_article_images_should_return_a_pair_of_wagtail_images_objects_with_fixed_resolution(self):
        article_images = self.load_initial_data_command._generate_article_images(1)

        self.assertEqual(len(article_images), 2)
        for image in article_images:
            self.assertTrue(isinstance(image, CustomImage))

        self._assert_wagtail_image_parameters_equal(article_images[0], 1668, 873, "cover_photo_1")
        self._assert_wagtail_image_parameters_equal(article_images[1], 2084, 598, "article_photo_1")

    def test_that_generate_wagtail_image_should_return_a_valid_wagtail_image_object_with_provided_parameters(self):
        wagtail_image = self.load_initial_data_command._generate_wagtail_image({"x": 640, "y": 480}, "Image")

        self._assert_wagtail_image_parameters_equal(wagtail_image, 640, 480, "Image")
