import random
from typing import Dict
from typing import Tuple

from django.conf import settings
from django.core.management import BaseCommand
from django.db import transaction
from django.utils.datetime_safe import datetime
from faker import Faker
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtail.core.models import Page
from wagtail.core.models import Site
from wagtail.images.models import Image as WagtailImage
from wagtailmarkdown.blocks import MarkdownBlock

from blog.models import BlogArticlePage
from blog.models import BlogCategorySnippet
from blog.models import BlogIndexPage
from common.helpers import create_image
from company_website.factories import BossFactory
from company_website.factories import EmployeeFactory
from company_website.models import Employees


class Command(BaseCommand):
    help = "Create initial sample data for Project Liberation application testing."

    bosses_limit = 2
    employees_limit = 20
    article_per_category = 15
    # Categories data
    categories = [
        {
            "title": "Blockchain",
            "seo_title": "Blockchain SEO title",
            "slug": "blockchain",
            "meta_description": "This is Blockchain Page",
            "keywords": "Blockchain, keywords",
        },
        {
            "title": "Culture",
            "seo_title": "Culture SEO title",
            "slug": "culture",
            "meta_description": "This is Culture Page",
            "keywords": "Culture, keywords",
        },
        {
            "title": "Development",
            "seo_title": "Development SEO title",
            "slug": "development",
            "meta_description": "This is Development Page",
            "keywords": "Development, keywords",
        },
        {
            "title": "Machine Learning",
            "seo_title": "Machine Learning SEO title",
            "slug": "machine-learning",
            "meta_description": "This is Machine Learning Page",
            "keywords": "Machine Learning, keywords",
        },
        {
            "title": "Technology",
            "seo_title": "Technology SEO title",
            "slug": "technology",
            "meta_description": "This is Technology Page",
            "keywords": "Technology, keywords",
        },
        {
            "title": "QA",
            "seo_title": "QA SEO title",
            "slug": "qa",
            "meta_description": "This is QA Page",
            "keywords": "QA, keywords",
        },
        {
            "title": "Project Management",
            "seo_title": "Project Management SEO title",
            "slug": "project-management",
            "meta_description": "This is Project Management Page",
            "keywords": "Project Management, keywords",
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):

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
                print(f"Boss {boss.name} created")
        # add 20 employees
        if len(Employees.objects.filter(boss=False)) == 0:
            for _ in range(0, self.employees_limit):
                employee = EmployeeFactory()
                front_image = create_image(300, 200, f"{employee.name}_1", settings.MEDIA_ROOT)
                back_image = create_image(300, 200, f"{employee.name}_2", settings.MEDIA_ROOT)
                employee.front_image = front_image
                employee.back_image = back_image
                employee.save()
                print(f"Employee {employee.name} created")

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
        fake = Faker()
        # Create category and for every category add 15 articles
        for category_parameters in self.categories:
            if not BlogCategorySnippet.objects.filter(**category_parameters).exists():
                blog_category_snippet = BlogCategorySnippet(**category_parameters)
                blog_category_snippet.save()
            else:
                blog_category_snippet = BlogCategorySnippet.objects.get(**category_parameters)

            for article_number in range(0, self.article_per_category + 1):
                blog_index_page = BlogIndexPage.objects.get(**blog_index_page_parameters)
                # base article parameters
                index = self.categories.index(category_parameters)
                author = employees[index]
                block = StreamBlock([("markdown", MarkdownBlock())])
                body = StreamValue(block, [("markdown", fake.sentence(nb_words=1000))])
                # article images
                rgb_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                wagtail_cover_photo = self._generate_wagtail_image({"x": 1668, "y": 873}, f"cover_photo_{index}_{article_number}", rgb_color=rgb_color)
                wagtail_article_photo = self._generate_wagtail_image({"x": 2084, "y": 598}, f"article_photo_{index}_{article_number}", rgb_color=rgb_color)
                # add article to database
                blog_article_page = BlogArticlePage(
                    title=fake.sentence(nb_words=5),
                    categories=[blog_category_snippet],
                    date=datetime.now(),
                    intro=fake.sentence(nb_words=30)[:250],
                    body=body,
                    author=author,
                    read_time=random.randint(1, 10),
                    views=0,
                    cover_photo=wagtail_cover_photo,
                    article_photo=wagtail_article_photo,
                    is_main_article=True,
                )
                blog_index_page.add_child(instance=blog_article_page)
                blog_article_page.save()

    def _generate_wagtail_image(self, resolution: Dict[str, int], name: str, rgb_color=None) -> WagtailImage:
        new_image = create_image(
            resolution["y"], resolution["x"], name, settings.MEDIA_ROOT, rgb_color=rgb_color
        )
        wagtail_new_image = WagtailImage.objects.create(
            title=name, file=new_image
        )
        wagtail_new_image.save()
        return wagtail_new_image