import random
from datetime import datetime
from typing import Any

import factory
from faker import Faker
from wagtail.core.blocks import RichTextBlock
from wagtail.core.blocks import StreamBlock
from wagtail.core.blocks import StreamValue
from wagtail.core.rich_text import RichText
from wagtail_factories import PageFactory

from blog.models import BlogArticlePage
from blog.models import BlogIndexPage


def generate_article_body() -> StreamValue:
    return StreamValue(
        StreamBlock([("paragraph", RichTextBlock())]),
        [
            (
                "paragraph",
                RichText(
                    (lambda text, tag: f"<{tag}>{text}</{tag}>")(
                        Faker().paragraph(nb_sentences=random.randint(30, 100)), "p"
                    )
                ),
            )
            for _ in range(random.randint(2, 7))
        ],
    )


class BlogIndexPageFactory(PageFactory):
    class Meta:
        model = BlogIndexPage


class BlogArticlePageFactory(PageFactory):
    class Meta:
        model = BlogArticlePage

    title = factory.Faker("sentence", nb_words=5)
    date = factory.LazyFunction(datetime.now)
    body = factory.LazyFunction(generate_article_body)
    author = factory.SubFactory("company_website.factories.EmployeeFactory")
    read_time = factory.Faker("pyint", min_value=5, max_value=20, step=5)
    recommended_articles = None
    views = 0
    is_main_article = False

    @classmethod
    def _create_instance(cls, model_class: Any, parent: Any, kwargs: Any) -> Any:
        instance = model_class(**kwargs)
        if parent is None:
            parent = BlogIndexPage.objects.all().first()
            if parent is None:
                parent = BlogIndexPageFactory()
        parent.add_child(instance=instance)
        return instance
