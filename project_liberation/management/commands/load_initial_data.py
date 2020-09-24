import random
from typing import Dict

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from django.utils.datetime_safe import datetime
from faker import Faker
from wagtail.core.blocks import PageChooserBlock
from wagtail.core.blocks import RichTextBlock
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtail.core.models import Page
from wagtail.core.models import Site
from wagtail.core.rich_text import RichText
from wagtail.images.models import Image as WagtailImage

from blog.constants import ArticleBodyBlockNames
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

    @transaction.atomic
    def handle(self, *args, **options):

        fake = Faker()
        # Add Testimonials
        if len(Testimonial.objects.all()) == 0:
            for index in range(0, self.testimonial_limit):
                testimonial = Testimonial(
                    name=fake.name()[:32],
                    position=fake.job()[:64],
                    quote=fake.sentence(nb_words=50)[:300],
                    image=create_image(
                        150, 150, f"testimonial_{index}", settings.MEDIA_ROOT, return_relative_path=True
                    ),
                )
                testimonial.save()
                print(f"{testimonial} testimonial successfully created")

        # Add Employees to Team Introduction Page
        # add 2 bosses
        if len(Employees.objects.filter(boss=True)) == 0:
            for _ in range(0, self.bosses_limit):
                boss = BossFactory()
                front_image = create_image(400, 267, f"{boss.name}_1", settings.MEDIA_ROOT)
                back_image = create_image(400, 267, f"{boss.name}_2", settings.MEDIA_ROOT)
                boss.front_image = front_image
                boss.back_image = back_image
                boss.save()
                print(f"Boss {boss.name} successfully created")
        # add 20 employees
        if len(Employees.objects.filter(boss=False)) == 0:
            for _ in range(0, self.employees_limit):
                employee = EmployeeFactory()
                front_image = create_image(300, 200, f"{employee.name}_1", settings.MEDIA_ROOT)
                back_image = create_image(300, 200, f"{employee.name}_2", settings.MEDIA_ROOT)
                employee.front_image = front_image
                employee.back_image = back_image
                employee.save()
                print(f"Employee {employee.name} successfully created")

        # Initiate Blog Index Page
        blog_index_page_parameters = {
            "title": "Blog",
            "meta_description": "Blog meta description",
            "keywords": "blog, keywords, test keywords",
        }
        if not BlogIndexPage.objects.filter(**blog_index_page_parameters).exists():
            blog_index_page = BlogIndexPage(**blog_index_page_parameters)
            Page.objects.get(title="Root").add_child(instance=blog_index_page)
            blog_index_page.save()
        else:
            blog_index_page = BlogIndexPage.objects.get(**blog_index_page_parameters)

        if not Site.objects.filter(root_page=blog_index_page):
            site = Site.objects.all().first()
            site.root_page = blog_index_page
            site.save()

        employees = Employees.objects.all()
        # Create articles
        last_id = 0
        for article_number in range(0, self.articles_limit):
            blog_index_page = BlogIndexPage.objects.get(**blog_index_page_parameters)
            # base article parameters
            index = article_number % employees.count()
            author = employees[index]
            block = StreamBlock([(ArticleBodyBlockNames.PARAGRAPH.value, RichTextBlock())])
            body = StreamValue(block, [(ArticleBodyBlockNames.PARAGRAPH.value, RichText(fake.sentence(nb_words=1000)))])
            # recommended articles
            if article_number > 3:
                articles_block = StreamBlock([("page", PageChooserBlock())])
                articles_data = []
                for i in range(3):
                    articles_data.append(("page", BlogArticlePage.objects.get(id=(last_id - i))))
                recommended_articles = StreamValue(articles_block, articles_data)
            else:
                recommended_articles = None
            # article images
            rgb_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            wagtail_cover_photo = self._generate_wagtail_image(
                {"x": 1668, "y": 873}, f"cover_photo_{article_number}", rgb_color=rgb_color
            )
            wagtail_article_photo = self._generate_wagtail_image(
                {"x": 2084, "y": 598}, f"article_photo_{article_number}", rgb_color=rgb_color
            )
            # add article to database
            blog_article_page = BlogArticlePage(
                title=fake.sentence(nb_words=5),
                date=datetime.now(),
                body=body,
                author=author,
                read_time=random.randint(1, 10),
                recommended_articles=recommended_articles,
                views=0,
                cover_photo=wagtail_cover_photo,
                article_photo=wagtail_article_photo,
                is_main_article=True,
            )
            blog_index_page.add_child(instance=blog_article_page)
            blog_article_page.save()
            last_id = blog_article_page.id

    @staticmethod
    def _generate_wagtail_image(resolution: Dict[str, int], name: str, rgb_color=None) -> WagtailImage:
        new_image = create_image(resolution["y"], resolution["x"], name, settings.MEDIA_ROOT, rgb_color=rgb_color)
        wagtail_new_image = WagtailImage.objects.create(title=name, file=new_image)
        wagtail_new_image.save()
        return wagtail_new_image
