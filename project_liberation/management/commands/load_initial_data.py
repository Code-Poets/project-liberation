import logging
import random
from typing import Dict

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from faker import Faker
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtail.core.models import Site
from wagtail.images.models import Image as WagtailImage

from blog.factories import BlogArticlePageFactory
from blog.factories import BlogIndexPageFactory
from blog.models import BlogArticlePage
from blog.models import BlogIndexPage
from common.helpers import create_image
from company_website.factories import BossFactory
from company_website.factories import EmployeeFactory
from company_website.models import Employees
from company_website.models import Testimonial


class Command(BaseCommand):
    help = "Create initial sample data for Project Liberation application testing."

    bosses_limit = 2
    employees_limit = 20
    testimonial_limit = 10
    articles_limit = 105
    max_paragraphs_per_article = 7
    min_paragraphs_per_article = 2
    max_recommended_articles = 5

    faker = Faker()

    @transaction.atomic
    def handle(self, *args, **options):
        self.add_testimonials()
        self.add_bosses()
        self.add_employees()
        self.initiate_blog_index_page()
        self.add_articles()

    def add_testimonials(self):
        if len(Testimonial.objects.all()) == 0:
            for index in range(0, self.testimonial_limit):
                testimonial = Testimonial(
                    name=self.faker.name()[:32],
                    position=self.faker.job()[:64],
                    quote=self.faker.sentence(nb_words=50)[:300],
                    image=create_image(
                        150, 150, f"testimonial_{index}", settings.MEDIA_ROOT, return_relative_path=True
                    ),
                )
                testimonial.save()
                logging.info(f"{testimonial} testimonial successfully created")

    def add_bosses(self):
        self._add_employee_objects(
            is_boss=True,
            limit=self.bosses_limit,
            factory=BossFactory,
            employee_type="Boss",
            picture_height=400,
            picture_width=267,
        )

    def add_employees(self):
        self._add_employee_objects(
            is_boss=False,
            limit=self.employees_limit,
            factory=EmployeeFactory,
            employee_type="Employee",
            picture_height=300,
            picture_width=200,
        )

    @staticmethod
    def _add_employee_objects(is_boss, limit, factory, employee_type, picture_height, picture_width):
        if len(Employees.objects.filter(boss=is_boss)) == 0:
            for _ in range(0, limit):
                employee = factory()
                employee.front_image = create_image(
                    picture_height, picture_width, f"{employee.name}_1", settings.MEDIA_ROOT
                )
                employee.back_image = create_image(
                    picture_height, picture_width, f"{employee.name}_2", settings.MEDIA_ROOT
                )
                employee.save()
                logging.info(f"{employee_type} {employee.name} successfully created")

    @staticmethod
    def initiate_blog_index_page():
        blog_index_page_parameters = {
            "title": "Blog",
            "meta_description": "Blog meta description",
            "keywords": "blog, keywords, test keywords",
        }
        if not BlogIndexPage.objects.filter(**blog_index_page_parameters).exists():
            blog_index_page = BlogIndexPageFactory(**blog_index_page_parameters)
        else:
            blog_index_page = BlogIndexPage.objects.get(**blog_index_page_parameters)

        if not Site.objects.filter(root_page=blog_index_page):
            site = Site.objects.all().first()
            site.root_page = blog_index_page
            site.save()

    def add_articles(self):
        employees = Employees.objects.all()
        for article_number in range(0, self.articles_limit):
            article_data = self._generate_article_data(article_number, employees)
            BlogArticlePageFactory(**article_data)
        self._add_recommendations_to_articles()

    def _generate_article_data(self, article_number, employees):
        (wagtail_cover_photo, wagtail_article_photo) = self._generate_article_images(article_number)
        index = article_number % employees.count()
        article_data = {
            "author": employees[index],
            "cover_photo": wagtail_cover_photo,
            "article_photo": wagtail_article_photo,
            "is_main_article": True,
        }
        return article_data

    def _add_recommendations_to_articles(self):
        for article in BlogArticlePage.objects.all():
            article.recommended_articles = self._generate_recommended_articles(article.id)
            article.save()
            logging.info(f"{len(article.recommended_articles)} recommended articles added to {article.title}")

    def _generate_recommended_articles(self, target_id):
        articles_block = StreamBlock([("page", PageChooserBlock())])
        article_ids = self._generate_list_of_article_ids_for_recommended_articles(target_id)
        recommended_articles = []
        for article_id in article_ids:
            recommended_articles.append(("page", BlogArticlePage.objects.get(id=article_id)))
        return StreamValue(articles_block, recommended_articles)

    def _generate_list_of_article_ids_for_recommended_articles(self, target_id):
        article_ids = []
        first_id = BlogArticlePage.objects.first().id
        last_id = BlogArticlePage.objects.last().id
        for _ in range(random.randint(0, self.max_recommended_articles)):
            article_id = random.randint(first_id, last_id)
            while article_id == target_id or article_id in article_ids:
                article_id = random.randint(first_id, last_id)
            article_ids.append(article_id)
        return article_ids

    def _generate_article_images(self, article_number):
        rgb_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        wagtail_cover_photo = self._generate_wagtail_image(
            {"x": 1668, "y": 873}, f"cover_photo_{article_number}", rgb_color=rgb_color
        )
        wagtail_article_photo = self._generate_wagtail_image(
            {"x": 2084, "y": 598}, f"article_photo_{article_number}", rgb_color=rgb_color
        )
        return wagtail_cover_photo, wagtail_article_photo

    @staticmethod
    def _generate_wagtail_image(resolution: Dict[str, int], name: str, rgb_color=None) -> WagtailImage:
        new_image = create_image(resolution["y"], resolution["x"], name, settings.MEDIA_ROOT, rgb_color=rgb_color)
        wagtail_new_image = WagtailImage.objects.create(title=name, file=new_image)
        return wagtail_new_image
